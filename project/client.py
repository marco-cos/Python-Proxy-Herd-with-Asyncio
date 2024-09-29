import asyncio
import time
import sys
import ports




Host = "127.0.0.1"
Servername = sys.argv[1]
Port = ports.dict[Servername]



async def clientmain() -> None:
    reader, writer = await asyncio.open_connection(Host, Port)

    if (len(sys.argv) > 1 and sys.argv[2] == "IAMAT"):
        sys.argv.insert(5,str(time.time()))
    writer.write(" ".join(sys.argv[2:]).encode())
    await writer.drain()

    data = await reader.read(4096)
    
    print(data.decode())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(clientmain())