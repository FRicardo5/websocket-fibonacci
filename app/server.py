from fastapi import WebSocket
from typing import Dict
from app.database.models.user import User
from sqlalchemy.orm import Session 
import logging
from datetime import datetime
import json
import asyncio
from starlette.websockets import WebSocketState

logger = logging.getLogger(__name__)    

class WSManagerServer:
    def __init__(self):
        self.clients: Dict[int, WebSocket] = {}
    async def connect(self, websocket: WebSocket, session: Session) -> int:
        await websocket.accept()
        try:
            user = User(name="User", connected=True)
            # count = session.query(User).count()
            session.add(user)
            session.commit()
            session.refresh(user)
            client_id = user.id
            self.clients[client_id] = websocket
            logger.info(f"novo cliente conectado: {client_id}")
            return client_id
        except Exception as e:
            logger.error(f"erro: {e}")
            #alterar para logg
            raise

    async def disconnect(self, client_id: int, session: Session):
        websocket = self.clients.pop(client_id, None)
        if websocket is not None:
            try:
                await websocket.close()
            except Exception:
                pass

        user = session.query(User).filter(User.id == client_id).first()
        if user is not None:
            user.connected = False
            user.disconnected_at = datetime.now()
            session.commit()
            session.refresh(user)

        logger.info(f"{client_id} desconectado")


    async def timer_send(self, session: Session):
        """ 
        atualizações de tempo em tempo para todos os clientes conectados
        """
        try:
            print("Iniciando tarefa de envio de atualizações de tempo")
            while True:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                time_message = {
                    "type": "time_update",
                    "timestamp": now
                }

                to_disconnect = []

                for client_id, websocket in list(self.clients.items()):
                    try:
                        if websocket.client_state == WebSocketState.CONNECTED:
                                await websocket.send_json(time_message)
                        else:
                                to_disconnect.append(client_id)
                    except Exception:
                            to_disconnect.append(client_id)

                for client_id in to_disconnect:
                    await self.disconnect(client_id, session)

                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Tarefa de envio de tempo cancelada")
        except Exception as e:
            # alterar para logging
            print(f"Erro na tarefa de envio de tempo: {e}")

        
        
    async def _send_fibonacci(self, client_id: int, n: int):
        """ 
        calcula e envia o número Fibonacci para o cliente
        """
        def fibonacci(n: int) -> int:
            if n <= 0:
                return 0
            elif n == 1:
                return 1
            else:
                return fibonacci(n-1) + fibonacci(n-2)

        result = fibonacci(n)
        await self.clients[client_id].send_json({
            "type": "fibonacci",
            "n": result
    })

    # gerencia msgs
    async def handle_message(self, client_id: int, message: str, session: Session):
        """
        processa mensagens recebidas dos clientes
        """
        if client_id not in self.clients:
            return

        try:
            print(f"Mensagem recebida do cliente {client_id}: {message}")
            # logg
            try:
                data = json.loads(message)
                msg_type = data.get("type", "")

                # verificar o tipo
                if msg_type == "fibonacci":
                    n = int(data.get("n", 0))
                    if n >= 0:
                        await self._send_fibonacci(client_id, n)
                    else:
                        await self.clients[client_id].send_json({
                            "type": "error",
                            "message": "Número deve ser não-negativo"
                        })

            except json.JSONDecodeError:
                if message.strip().isdigit():
                    n = int(message)
                    await self._send_fibonacci(client_id, n)
                else:
                    await self.clients[client_id].send_json({
                        "type": "error",
                        "message": "Comando não reconhecido"
                    })

        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            await self.disconnect(client_id, session)
