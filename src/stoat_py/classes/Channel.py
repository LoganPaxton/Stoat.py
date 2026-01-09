import ulid
from typing import List
from datetime import datetime
from .Message import Message

class Channel:
    def __init__(self, client, data: dict):
        self.client = client
        self.id = data.get("_id")
        self.name = data.get("name")
        self.type = data.get("channel_type")
        self.server_id = data.get("server")
        self.last_message_id = data.get("last_message_id")
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

    async def fetch_webhooks(self) -> List[dict]:
        """Get all webhooks for this channel"""
        response = await self.client.http.get(f"/channels/{self.id}/webhooks")
        return response.json()

    async def send_message(self, content: str, silent: bool = False) -> Message:
        """Send a message to a channel"""
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
        
        return Message(self.client, response.json())

    async def fetch_message(self, message_id: str) -> Message:
        """Fetch a specific message by its ID"""
        response = await self.client.http.get(f"/channels/{self.id}/messages/{message_id}")
        return Message(self.client, response.json())

    async def delete(self, leave_silently: bool = False):
        """Delete the channel or leave the group"""
        params = {"leave_silently": str(leave_silently).lower()}
        await self.client.http.delete(f"/channels/{self.id}", params=params)

    async def set_permissions(self, role_id: str = "default", permissions: int = 0):
        """Set role permissions for this channel"""
        payload = {"permissions": permissions}
        response = await self.client.http.put(
            f"/channels/{self.id}/permissions/{role_id}", 
            json=payload
        )
        return response.json()
    
    async def edit_channel(self, name=None):
        if name is None:
            name = self.name
        
        payload = {
            "name": name
        }
        await self.client.http.patch(f"/channels/{self.id}", json=payload)
    
    async def add_recipient(self, user_id: str):
        await self.client.http.put(f"/channels/{self.id}/recipients/{user_id}")
        
    async def remove_recipient(self, user_id: str):
        await self.client.http.delete(f"/channels/{self.id}/recipients/{user_id}")
        

    def __repr__(self):
        return f"<Channel name='{self.name}' id='{self.id}' type='{self.type}'>"