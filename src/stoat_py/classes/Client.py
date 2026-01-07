import asyncio
import httpx
from stoat_py.utils.heartbeat import Gateway 

class Client:
    def __init__(self):
        self.token = ""
        self.events = {} 
        self.http = httpx.AsyncClient(base_url="https://api.stoat.chat")

    def event(self, func):
        self.events[func.__name__] = func
        return func

    async def dispatch(self, event_name: str, *args, **kwargs):
        if event_name in self.events:
            func = self.events[event_name]
            if asyncio.iscoroutinefunction(func):
                await func(*args, **kwargs)
            else:
                func(*args, **kwargs)

    async def start(self, token: str):
        self.token = token
        
        self.http.headers.update({
            "X-Bot-Token": self.token,
            "Content-Type": "application/json"
        })

        res = await self.http.get("/")
        config = res.json()
        ws_url = config.get("ws", "wss://stoat.chat/events")
        
        self.gateway = Gateway(ws_url, self.token, self.dispatch)
        await self.gateway.connect()