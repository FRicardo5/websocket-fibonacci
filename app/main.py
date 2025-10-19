from fastapi import WebSocket, FastAPI, Depends
from app.wsmanager import manager
from datetime import datetime
import asyncio
import uuid
from app.database.database import create, init, get_session
from app.database.models.user import User
from sqlalchemy.orm import Session

clients = []
app = FastAPI()

@app.websocket("/wsmanager/")
async def wsocket(websocket: WebSocket, session: Session = Depends(get_session)):
    await manager.connect(websocket)

    contador = session.query(User).count()
    client_id = contador + 1
    clients.append({"id": client_id, "websocket": websocket})

    user = User(name=f"User_{client_id}", connected=True)
    session.add(user)
    session.commit()
    session.refresh(user)
    client_id = user.id





