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
    
    if stripped == "ping":
        channel = Channel(client, {"_id": msg.channel_id})
        await channel.send_message("Pong!")
    elif stripped == "delete":
        channel = Channel(client, {"_id": "01KEG7SZF0F956F116FXKPFS2M"})
        await channel.delete()
    elif stripped == "edit":
        channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
        channel.edit_channel("Main")
        
    

asyncio.run(client.start(TOKEN))