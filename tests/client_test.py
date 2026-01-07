import asyncio
import dotenv
import os
from stoat_py.classes import Channel, Client, Message

dotenv.load_dotenv()

client = Client()
TOKEN = os.environ.get('BOT_TOKEN')

@client.event
async def on_ready(data):
    bot_user = next((u for u in data['users'] if 'bot' in u), None)
    print(f"Logged in as {bot_user['username']}")
    
    """ channel = Channel(client, {"_id": "01KE7HCF6VZACAWNEJVADFZJD0"})
    members = await channel.fetch_members()
    print(members) """
    
    """ channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
    webhook = await channel.create_webhook("stoat.py test")
    print(webhook) """

@client.event
async def on_message(data):
    msg : str = data['content']
    stripped = msg[1:]
    if msg.startswith('!'):
        if stripped == "ping":
            channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
            await channel.send_message("Pong!")
    #print(f"[+] New message. \n [-]Content: {data['content']}\n [-]Message ID: {data['_id']}")


asyncio.run(client.start(TOKEN))