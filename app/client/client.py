import asyncio
import websockets

async def listen(user_id: int):
    uri = f"ws://localhost:8000/wsmanager/{user_id}"
    print(f"Conectando a {uri}...")

    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado!\n")

            while True:
                message = await websocket.recv()
                print(message)

    except websockets.ConnectionClosedOK:
        print("Conexão encerrada pelo servidor.")
    except websockets.ConnectionClosedError as e:
        print(f"Conexão encerrada com erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def main():
    try:
        user_id = int(input("Digite o ID do usuário: "))
        asyncio.run(listen(user_id))
    except ValueError:
        print("ID inválido. Digite um número inteiro.")
    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")

if __name__ == "__main__":
    main()
