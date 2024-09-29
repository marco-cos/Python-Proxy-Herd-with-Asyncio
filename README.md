# Proxy Herd with Asyncio

## Overview
This project demonstrates the use of Python's `asyncio` module to implement a server herd architecture, simulating a news service similar to Wikimedia's platform. The key focus is on using `asyncio` for inter-server communication, allowing the propagation of client location data across multiple servers and responding to client queries using the Google Places API. Project for UCLA CS 131 class.

## Features
- **Server Herd Architecture**: Five servers ('Bailey', 'Bona', 'Campbell', 'Clark', 'Jaquez') communicate bidirectionally using TCP, forwarding location data without requiring the central database.
- **Client Location Updates**: Clients can send location data using the `IAMAT` command, which is propagated to other servers in the herd.
- **Nearby Places Query**: Clients can query nearby places around a location using the `WHATSAT` command, fetching information from the Google Places API.
- **Flooding Algorithm**: A simple flooding algorithm ensures location updates are shared across servers.
- **Error Handling**: Servers respond to invalid commands with an error message and log all interactions.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd proxy-herd-asyncio
   ```
2. Install required dependencies:
   ```bash
   pip install aiohttp
   ```

## Running the Servers
To start a server, run the following command:
```bash
python3 server.py <server_name>
```
Replace `<server_name>` with the ID of the server (Bailey, Bona, Campbell, Clark, or Jaquez).

Each server runs on an assigned port. Make sure to use your assigned ports.

## Commands
- **IAMAT**: Sends location data to a server.
   ```bash
   IAMAT <client_id> <latitude><longitude> <timestamp>
   ```
   Example:
   ```bash
   IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 1621464827.959498503
   ```

- **WHATSAT**: Queries nearby places for a client’s location.
   ```bash
   WHATSAT <client_id> <radius_in_km> <max_results>
   ```
   Example:
   ```bash
   WHATSAT kiwi.cs.ucla.edu 10 5
   ```

## Flooding Algorithm
Location updates are propagated between servers through a simple flooding algorithm. Each server logs received updates and forwards them to its neighboring servers. Servers prevent redundant updates by tracking message history.

## Logging
Each server logs all messages, including client interactions and connections to other servers. Logs are stored in the server’s working directory.

## Limitations
- **Single-Threaded**: The `asyncio` module is single-threaded, meaning the implementation may struggle with high traffic loads or multi-core CPUs.
- **Scaling**: This prototype is designed for small-scale testing, and may require modification for large-scale use.
- **Performance**: While efficient for asynchronous I/O, Python's performance may lag behind lower-level languages in more demanding scenarios.

## Conclusion
The project demonstrates the feasibility of using `asyncio` to implement a server herd. While effective for small-scale applications, its limitations in multi-threading and performance may hinder large-scale deployments.

For detailed analysis, see the accompanying report.

## References
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp documentation](https://docs.aiohttp.org/en/stable/)