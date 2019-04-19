#!/usr/bin/python3

"""
Simple tcp server, asks for username and password and checks the pass CRC32
See https://docs.python.org/3.7/library/asyncio-stream.html#tcp-echo-server-using-streams
"""

import asyncio
from zlib import crc32

HOST = "127.0.0.1"
PORT = 8888

GOAL_CRC32 = 3487400559  # pizza

MESSAGE = """
              xxxxxxx
XXXXXXXXXXXX x.......'XXXXXXXXXXXX
   XXXXXXXX x..o...o..x  XXXXXX
    XXXXXXXX x..........XXXXXX
     XXXXXXXXXX ....  .XXXXXX...,
       XXXXXXX   ;    xXXXXx,....;
        XXXXXXXX     XXXXXXX ;....;
         XXXXXXXX  XXXXXXX ;.....;
        ..XXXXXXXXXXXXXX .......;
    ......,XXXXXXXXXXXX ......,
  ....,';   XXXXXXXXXX
 :.,'..:     XXXXXXXXx
 :'....     XXXXXXXXXXX    .
 :......, xXXXXXXXXXXXXX   ..
  ......:xXXXXX     XXXXX '...
   '....XXXXX:................
     ;XXXXXX:.................;
    xXXXXXx             XXXXX
  xXXXXXXx              xXXXXXx
XXXXXXXXXXXX           XXXXXXXXXX


"""


async def handle_connection(reader, writer):
    # Send the snake
    writer.write(MESSAGE.encode())
    await asyncio.sleep(0.2)
    writer.write(b"Please login to continue\n\n")
    await asyncio.sleep(0.5)
    await writer.drain()
    username = b""
    password = b""
    try:
        writer.write(b"Username: ")
        username = await asyncio.wait_for(reader.read(1024), timeout=60)
        writer.write(b"Password: ")
        password = await asyncio.wait_for(reader.read(1024), timeout=60)
    except asyncio.TimeoutError:
        print("Timeout while reading username or password")

    print(f"Tried to login with username: {username} and password: {password}")
    if crc32(password.rstrip()) == GOAL_CRC32:
        writer.write(b"Access granted!\n")
    else:
        writer.write(b"Access denied!\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, "127.0.0.1", 8888)

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
