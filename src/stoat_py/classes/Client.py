import asyncio
import httpx
import inspect
from stoat_py.utils.heartbeat import Gateway 

class Client:
    def __init__(self):
        # Connection/Auth state
        self.token = ""
        self.events = {} 
        self.http = httpx.AsyncClient(base_url="https://api.stoat.chat")
        self.configuration = None
        self.gateway = None
        
        # Identity Properties (populated on Ready)
        self.id = None
        self.username = None
        self.discriminator = None
        self.display_name = None
        self.avatar = None
        self.bot_owner_id = None

    def event(self, func):
        """Decorator for event registration"""
        self.events[func.__name__] = func
        return func

    async def dispatch(self, event_name: str, *args, **kwargs):
        """Internal emitter to trigger registered events"""
        if event_name in self.events:
            func = self.events[event_name]
            
            sig = inspect.signature(func)
            params = sig.parameters
            
            if len(params) == 0:
                call_args = []
                call_kwargs = {}
            else:
                call_args = args
                call_kwargs = kwargs
            
            if asyncio.iscoroutinefunction(func):
                await func(*call_args, **call_kwargs)
            else:
                func(*call_args, **call_kwargs)

    def _handle_ready(self, data: dict):
        """
        Internal: Populates self.[property] from the Ready data blob.
        Matches the bot user inside the users list.
        """
        bot_user = next((u for u in data.get('users', []) if 'bot' in u), None)
        
        if bot_user:
            self.id = bot_user.get('_id')
            self.username = bot_user.get('username')
            self.discriminator = bot_user.get('discriminator')
            self.display_name = bot_user.get('display_name')
            self.avatar = bot_user.get('avatar')
            if 'bot' in bot_user:
                self.bot_owner_id = bot_user['bot'].get('owner')

    async def start(self, token: str):
        self.token = token
        
        self.http.headers.update({
            "X-Bot-Token": self.token,
            "Content-Type": "application/json"
        })

        res = await self.http.get("/")
        self.configuration = res.json()
        
        ws_url = self.configuration.get("ws", "wss://stoat.chat/events")
        
        original_dispatch = self.dispatch
        
        async def internal_dispatch(event_name, data):
            if event_name == "on_ready":
                self._handle_ready(data)
            await original_dispatch(event_name, data)

        self.gateway = Gateway(ws_url, self.token, internal_dispatch, self)
        await self.gateway.connect()

    def __repr__(self):
        return f"<Client username={self.username} id={self.id}>"