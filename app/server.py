from fastapi import WebSocket, Depends
from typing import Dict
from app.database.models.user import User
from app.database.database import get_session
from sqlalchemy.orm import Session 
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)    

class WSManagerServer:
    def __init__(self):
        self.clients: Dict[int, WebSocket] = {}
        self.last_time_see = {}

    async def connect(self, websocket: WebSocket, client_id: int, session: Session):
        await websocket.accept()
        self.clients[client_id] = websocket
        logger.info(f"Novo cliente conectado: {client_id}")

        try:
            contador = session.query(User).count()
            client_id = contador + 1
            user = User(name=f"User_{client_id}", connected=True)
            session.add(user)
            session.commit()
            session.refresh(user)
            client_id = user.id
            logger.info(f"{client_id} conectado")

        except Exception as e:
            logger.error(f"erro: {e}")



    async def disconnect(self, websocket: WebSocket, client_id: int, session: Session) :
        if client_id in self.clients:
            try:
                await websocket.close()
            except Exception as e:
                pass

            user = session.query(User).filter(User.id == client_id).first()
            user.connected = False
            user.disconnected_at = datetime.now()
            session.commit()
            session.refresh(user)

            self.clients.pop(client_id)
            logger.info(f"{client_id} desconectado")


    async def handle_messages(self, websocket: WebSocket, client_id: int, session: Session):
        if client_id not in self.clients:
            logger.error(f"Cliente {client_id} não encontrado")
            return

        data = await websocket.receive_text()
        try:
            data = json.loads(data)
            print(f"Mensagem recebida {client_id}: {data}")

            try:
                msg_type = data["type"]

                if msg_type == "fibonacci":
                    n = int(data["n"])
                    if n >= 0:
                        await self._send_fibonacci(client_id, n)
                    else:
                        await self.clients[client_id].send_json({
                            "type": "error",
                            "message": "Número deve ser não-negativo"
                        })
            except Exception as e:
                logger.error(f"erro: {e}")
        except Exception as e:
            logger.error(f"erro: {e}")
           

    async def broadcast(self, message: str):
        for connection in self.clients:
            await connection.send_text(message)

manager = WSManagerServer()