import asyncio
import websockets

# WebSocket server URL
ROBOCODERS_WS_URL = 'wss://www.robocoders.ai/ws'

async def forward_messages(client_ws, server_ws):
    async for message in client_ws:
        print(f"Forwarding message from client to server: {message}")
        await server_ws.send(message)

async def handle_client(client_ws):
    async with websockets.connect(ROBOCODERS_WS_URL) as server_ws:
        client_to_server_task = asyncio.create_task(forward_messages(client_ws, server_ws))
        server_to_client_task = asyncio.create_task(forward_messages(server_ws, client_ws))
        done, pending = await asyncio.wait(
            [client_to_server_task, server_to_client_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()

async def main():
    async with websockets.serve(handle_client, 'localhost', 7860):
        print("WebSocket server is listening on ws://localhost:7860")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
