import asyncio
import json
import time
import websockets
from stoat_py.utils.errors import AuthenticationError

class Gateway:
    def __init__(self, ws_url, token, dispatch_func):
        self.ws_url = ws_url
        self.token = token
        self.dispatch = dispatch_func 
        self.websocket = None
        self.heartbeat_interval = 20

    async def connect(self):
        ws_url = f"{self.ws_url}?format=json"
        async with websockets.connect(ws_url) as ws:
            self.websocket = ws
            if await self.authenticate():
                heartbeat_task = asyncio.create_task(self.heartbeat_loop())
                try:
                    await self.listen()
                finally:
                    heartbeat_task.cancel()

    async def authenticate(self):
        await self.websocket.send(json.dumps({
            "type": "Authenticate",
            "token": self.token
        }))
        
        raw_response = await self.websocket.recv()
        response = json.loads(raw_response)

        if response.get("type") == "Authenticated":
            return True
        raise AuthenticationError("Failed to authenticate with Stoat Gateway.")

    async def heartbeat_loop(self):
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            try:
                await self.websocket.send(json.dumps({"type": "Ping", "data": int(time.time())}))
            except Exception: break

    async def listen(self):
        async for message in self.websocket:
            data = json.loads(message)
            event_type = data.get("type")

            if event_type == "Ready":
                await self.dispatch("on_ready", data)
                
            elif event_type == "Message":
                await self.dispatch("on_message", data)
                
            elif event_type == "Pong":
                await self.dispatch("on_heartbeat", data)