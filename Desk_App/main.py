import asyncio
import websockets
import json
import time

async def handle_connection():
    uri = "ws://localhost:3031"

    while True:
        try:
            print("Connecting to server...")
            async with websockets.connect(uri) as ws:
                print("Connected!")

                # send initial message (optional)
                await ws.send(json.dumps({"type": "hello", "client": "desk_app"}))

                while True:
                    msg = await ws.recv()
                    print("Received:", msg)

        except Exception as e:
            print("Connection lost:", e)
            print("Reconnecting in 2 seconds...")
            time.sleep(2)  # slow down reconnect loop

asyncio.run(handle_connection())
