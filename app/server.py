from fastapi import WebSocket, Depends
from typing import Dict
from app.database.models.user import User
from app.database.database import get_session
from sqlalchemy.orm import Session 
import logging

logger = logging.getLogger(__name__)    

class WSManagerServer:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}
        self.last_time_see = {}

    async def connect(self, websocket: WebSocket, session: Session = Depends(get_session)):
        await websocket.accept()
        self.clients.append(websocket)
        logger.info(f"Novo cliente conectado: {websocket.client.host}")

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


    def disconnect(self, websocket: WebSocket, client_id: int, session: Session = Depends(get_session)):
        if client_id in self.clients:
            try:
                await websocket.close()
            except Exception as e:
                pass
            self.clients.pop(client_id)
            user = session.query(User).filter(User.id == client_id).first()
            user.connected = False
            user.disconnected_at = datetime.now()
            session.commit()
            session.refresh(user)
            logger.error(f"Cliente {client_id} desconectado")
        self.clients.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.clients:
            await connection.send_text(message)

manager = WSManagerServer()