import asyncio
import dotenv
import os
from stoat_py.classes import Client, Message, Channel

dotenv.load_dotenv()

client = Client()
TOKEN = os.environ.get('BOT_TOKEN')
PREFIX = "!"

CMD_LIST = {
    'ping'
}

@client.event
async def on_ready():
    print(f"Logged in as {client.username}#{client.discriminator}")

@client.event
async def on_message(msg: Message):
    content = msg.content
    stripped = msg.content[1:].lower() # Remove the prefix, and convert to lowercase for easier command matching
    if not content.startswith(PREFIX):
        return
    
    print(stripped)
    if stripped == "ping":
        channel = Channel(client, {"_id": msg.channel_id})
        await channel.send_message("Pong!")
    

asyncio.run(client.start(TOKEN))