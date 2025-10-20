from websockets.exceptions import ConnectionClosed
from websockets.legacy.client import WebSocketClientProtocol
import asyncio
import websockets
import json
import sys
import os
from uuid import uuid4

PROMPT = "<-"

async def send(ws: WebSocketClientProtocol, loop):
    """ envia mensagens para servidor """
    try:

        while True:
            user_input = await loop.run_in_executor(None, input, PROMPT)
            user_input = user_input.strip()

            # recebo o numero e defino o tipo de mensagem
            n = int(user_input)
            await ws.send(json.dumps({"type": "fibonacci", "n": n}))
    except ConnectionClosed as e:
        print(f"Servidor desconectou: {e}")



    except Exception as e:

        print(f"Erro: {e}")


async def rcv(ws: WebSocketClientProtocol):
    """ receb mensagens do servidor """

    try:

        async for msn in ws:
            try:
                data = json.loads(msn)
            except Exception:
                data = None

            # print mensagens formatadas
            if isinstance(data, dict) and data.get("type") == "time_update":
                print(f"->{data}\n", end="", flush=True)
            else:
                print(f"<-: {msn}   ", end="", flush=True)
    except ConnectionClosed as e:
        print(f"Servidor desconectou: {e}")



    except Exception as e:
        print(f"Erro inesperado na recepção: {e}")


async def conn(username: str = "client2"):
    url = "ws://localhost:8000/wsmanager/"
    async with websockets.connect(url) as ws:
            loop = asyncio.get_event_loop()

            await asyncio.gather(rcv(ws), send(ws, loop))




if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:

            asyncio.run(conn(sys.argv[1]))
        else:
            _id = str(uuid4())
            asyncio.run(conn(f"user-{_id}"))


    except KeyboardInterrupt:
        print("-> desconectado.")
