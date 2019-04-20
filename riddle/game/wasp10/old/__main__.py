"""
Simple tcp server, asks for username and password and checks the pass CRC32
See https://docs.python.org/3.7/library/asyncio-stream.html#tcp-echo-server-using-streams

Run with python3 -m riddle.game.wasp10.old to start
"""

import asyncio
import hashlib
from base64 import b64encode
from . import success_message


HOST = "0.0.0.0"
PORT = 8888


def digest(data):
    return int.from_bytes(hashlib.blake2b(data, digest_size=3).digest(), 'big')


GOAL_USER = b'monty-python'
GOAL_DIGEST = digest(b'flying circus')


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

    username = username.strip()
    password = password.strip()

    print(f"Tried to login with username: {username} and password: {password}")
    if username == GOAL_USER and digest(password) == GOAL_DIGEST:
        writer.write(b"Access granted!\n")
        writer.write(b64encode(success_message.encode()))
    else:
        writer.write(b"Access denied!\n")

    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
