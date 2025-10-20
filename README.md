## WebSocket Fibonacci

cliente-servidor websocket que envia aos clientes conectados data e hora cada segundo.:
- Envia a data/hora atual a cada segundo para todos os clientes
- Gerencia usuários conectados (PostgreSQL)
- Calcula Fibonacci e responde apenas ao solicitante

### Requisitos
- Python 3.11+
- Docker (opcional) e Docker Compose

### Rodando com Docker (recomendado)
```bash
docker compose up --build
```
Servidor: `http://localhost:8000`  |  WebSocket: `ws://localhost:8000/wsmanager/`

Cliente de teste (em outro terminal):
```bash
python client/client.py
```

### Rodando localmente (sem Docker)
1) Criar e ativar venv (opcional):
```bash
python -m venv .venv && .venv/Scripts/activate
```
2) Instalar dependências:
```bash
pip install -r requirements.txt
```
3) Garantir que um PostgreSQL esteja rodando e exportar variáveis (se necessário):
```bash
set DB_USER=postgres
set DB_PASSWORD=senha123
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=websocket_fibonacci
```
4) Subir o servidor:
```bash
uvicorn app.main:app --reload
```
5) Executar o cliente:
```bash
python client/client.py
```