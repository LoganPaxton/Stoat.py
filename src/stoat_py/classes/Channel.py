import ulid
from typing import Union, List
from datetime import datetime

class Channel:
    def __init__(self, client, data: dict):
        self.client = client
        self.id = data.get("_id")
        self.name = data.get("name")
        self.type = data.get("channel_type")
        self.server_id = data.get("server")
        self._raw_data = data
        self.ULID = ulid.ULID()

    async def fetch_members(self) -> List[dict]:
        """Fetch users in this channel (Groups/DMs)"""
        response = await self.client.http.get(f"/channels/{self.id}/members")
        return response.json()

    async def create_webhook(self, name: str, avatar_id: str = None) -> dict:
        """Create a new webhook for this channel"""
        payload = {"name": name}
        if avatar_id:
            payload["avatar"] = avatar_id
            
        response = await self.client.http.post(
            f"/channels/{self.id}/webhooks", 
            json=payload
        )
        return response.json()

    async def send_message(self, content: str, silent: bool = False) -> dict:
        """
        Send a message to this channel.
        Replicates the @silent and Idempotency logic from JS.
        """
        payload = {"content": content}
        
        if silent or content.startswith("@silent "):
            if content.startswith("@silent "):
                payload["content"] = content[8:]
            payload["flags"] = 1

        idempotency_key = str(self.ULID.from_datetime(datetime.now()))
        
        headers = {"Idempotency-Key": idempotency_key}
        
        response = await self.client.http.post(
            f"/channels/{self.id}/messages",
            json=payload,
            headers=headers
        )
        return response.json()

    async def delete(self, leave_silently: bool = False):
        """Delete the channel or leave the group"""
        params = {"leave_silently": leave_silently}
        await self.client.http.delete(f"/channels/{self.id}", params=params)

    def __repr__(self):
        return f"<Channel name={self.name} id={self.id} type={self.type}>"