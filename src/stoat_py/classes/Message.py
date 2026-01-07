class Message:
    def __init__(self, client, data: dict):
        self.client = client
        self.id = data.get("_id")
        self.channel_id = data.get("channel")
        self.content = data.get("content")
        self.author_id = data.get("author")
        self._raw_data = data

    async def edit(self, content: str):
        """Edit this message"""
        payload = {"content": content}
        res = await self.client.http.patch(
            f"/channels/{self.channel_id}/messages/{self.id}", 
            json=payload
        )
        self.content = content
        return self

    async def delete(self):
        """Delete this message"""
        await self.client.http.delete(f"/channels/{self.channel_id}/messages/{self.id}")

    async def pin(self):
        """Pin this message"""
        await self.client.http.post(f"/channels/{self.channel_id}/messages/{self.id}/pin")
        return self

    async def unpin(self):
        """Unpin this message"""
        await self.client.http.delete(f"/channels/{self.channel_id}/messages/{self.id}/pin")
        return self

    async def add_reaction(self, emoji: str):
        """Add a reaction to this message"""
        await self.client.http.put(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}")
        return self

    async def remove_reaction(self, emoji: str):
        """Remove a reaction from this message"""
        await self.client.http.delete(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}")
        return self

    async def clear_reactions(self):
        """Remove all reactions from this message"""
        await self.client.http.delete(f"/channels/{self.channel_id}/messages/{self.id}/reactions")
        return self
    

    def __repr__(self):
        return f"<Message id={self.id} author={self.author_id}>"