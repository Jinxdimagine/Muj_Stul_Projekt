import asyncio
import websockets
import json
import threading
import time

class WebSocketClient:
    def __init__(self, uri, on_message=None):
        """
        uri: ws://localhost:3031
        on_message: callback function to send received messages to GUI
        """
        self.uri = uri
        self.on_message = on_message
        self.running = True
        self.ws = None

    async def connect(self):
        while self.running:
            try:
                async with websockets.connect(self.uri) as ws:
                    self.ws = ws
                    print("Connected to server")

                    # Optionally send a hello message
                    await self.send({"type": "desk_app_connected"})
                    while self.running:
                        message = await ws.recv()
                        data = json.loads(message)
                        # Send message to GUI callback
                        if self.on_message:
                            self.on_message(data)
            except Exception as e:
                print("Connection lost, retrying in 2s...", e)
                await asyncio.sleep(2)

    def start(self):
        # Run websocket in a separate thread
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        asyncio.run(self.connect())

    async def send(self, data):
        if self.ws:
            try:
                await self.ws.send(json.dumps(data))
            except Exception as e:
                print("Send failed:", e)

    def send_sync(self, data):
        asyncio.run(self.send(data))

    def stop(self):
        self.running = False