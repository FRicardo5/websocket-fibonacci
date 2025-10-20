from fastapi import WebSocket, FastAPI
from app.server import WSManagerServer
from app.database.database import init
import asyncio
import logging
from contextlib import asynccontextmanager
from app.database.database import get_session

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = WSManagerServer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando o banco de dados")
    session = next(get_session())
    init()
    asyncio.create_task(manager.timer_send(session))
    print("Banco de dados iniciado")
    yield
    print("Finalizando aplicação")

app = FastAPI(lifespan=lifespan)

@app.websocket("/wsmanager/")
async def websocket_endpoint(websocket: WebSocket):
    session = next(get_session())
    client_id = await manager.connect(websocket, session)

    try:
        await websocket.send_json({
            "type": "welcome",
            "message": "Conectado ao servidor WebSocket",
            "client_id": client_id
        })

        while True:
            message = await websocket.receive_text()
            await manager.handle_message(client_id, message, session)

    except Exception as e:
        print(f"Erro na conexão WebSocket: {e}")
        await manager.disconnect(client_id, session)