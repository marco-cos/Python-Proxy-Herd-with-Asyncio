import asyncio
import sys
import time
import aiohttp
import ports
import json
import re
import logging

Servername = sys.argv[1]

logger = logging.getLogger(__name__)
logging.basicConfig(filename=f"{Servername}.log", level=logging.INFO)

Clients = {}
Sentmessages = set()

def log(l): 
    print(l)
    logger.info(l)


ApiKey = "APIKEYHERE"


Host = "127.0.0.1"
Port = ports.dict[Servername]

async def APIrequest(lat, long, radius):
    link = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius={radius}&key={ApiKey}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(link) as r:
            ret = await r.json()
            return ret

async def propogateIAMAT(unsplitmsg, output, clientID):
    if unsplitmsg not in Sentmessages:
        for server, port in ports.dict.items():
            if server in ports.communicable[Servername]:
                try:
                    Sentmessages.add(unsplitmsg)
                    reader, writer = await asyncio.open_connection(Host, port)
                    writer.write(unsplitmsg.encode())
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()
                    log(f"New connection to server {server} in order to propogate IAMAT message")
                except:
                    log(f"Dropped connection: Could not reach {server} for propogation")
    else:
        return

def formatJSON(jsn, upperbound):
    dict(jsn)
    jsn["results"] = jsn["results"][:upperbound]
    jsn = json.dumps(jsn, indent=2)
    jsn = re.sub("[\n]{2,}","\n",jsn)
    jsn = jsn.rstrip("\n")
    return jsn

async def handleWHATSAT(unsplitmsg):
    message = unsplitmsg.split(" ")
    if (len(message) !=4 or message[1] not in Clients):
        return f"? {message}"
    else:
        clientID = message[1]
        radius = message[2]
        upperbound = int(message[3])
        apiret = await APIrequest(Clients[clientID][1], Clients[clientID][2], radius)
        return f"{Clients[clientID][0]}\n{formatJSON(apiret,upperbound)}\n\n"

async def handleIAMAT(unsplitmsg):
    message = unsplitmsg.split(" ")
    if (len(message) != 4):
        output = f"? {message}"
    else:   
        clientID = message[1]
        location = message[2]
        clienttime = message[3]

        rawrettime = time.time() - float(clienttime)
        rettime = f"+{str(rawrettime)[:11]}" if rawrettime > 0 else f"-{str(rawrettime)[:11]}"

        lat = location[:max(location[1:].find("+"), location[1:].find("-"))+1]
        long = location [max(location[1:].find("+"), location[1:].find("-"))+1:]

        output = f"AT {Servername} {rettime} {" ".join(message[1:])}"

        await propogateIAMAT(unsplitmsg, output, clientID)

        Clients[clientID] = [output, lat, long, unsplitmsg]
    
    return output
    


async def mainfunc(reader, writer):
    data = None
    
    while data != b"quit":
        data = await reader.read(4096)
        if not data:
            break
        msg = data.decode()

        addr, port = writer.get_extra_info("peername")
        
        log(f"Recieved message: {msg}")
        if (len(msg)>0 and msg.split(" ")[0] == "IAMAT"):
            #print("Recieved IAMAT Message")
            output = str(await handleIAMAT(msg))
        elif (len(msg)>0 and msg.split(" ")[0] == "WHATSAT"):
            #print("Recieved WHATSAT Message")
            output = await handleWHATSAT(msg)
        else:
            output = str(f"? {msg}")
    
        log(f"Outputting response: {output}")

        writer.write(output.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def server():
    s = await asyncio.start_server(mainfunc, Host, Port)
    async with s:
        await s.serve_forever()

if __name__ == "__main__":
    looper = asyncio.new_event_loop()
    looper.run_until_complete(server())
