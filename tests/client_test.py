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
    
    """ channel = Channel(client, {"_id": "01KE7HCF6VZACAWNEJVADFZJD0"})
    msg_id = "01KEAZ19JW33QEHGP5VT6XF0BG"
    await channel.unpin_message(msg_id) """
    
    """ channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
    webhooks = await channel.fetch_webhooks()
    print(webhooks) """
    
    """ channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
    emoji = "🔥"
    await channel.clear_reactions("01KE7VZCDHME9S3Q06DCP2TED4") """
    
    """ channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
    await channel.delete_message("01KED7AKPE4E46VBW7DAWMFH9G") """
    
    channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
    #await channel.send_message("This message should be editied.")
    res = await channel.edit_message("01KED7PDFNV7KYEJPBVK18MDXV", "This message should be edited.")
    print(res)

@client.event
async def on_message(data):
   """  msg : str = data['content']
    stripped = msg[1:]
    if msg.startswith('!'):
        if stripped == "ping":
            channel = Channel(client, {"_id": "01KE7FGF0ENHN49SQVPN3WVGVK"})
            await channel.send_message("Pong!") """
    #print(f"[+] New message. \n [-]Content: {data['content']}\n [-]Message ID: {data['_id']}")


asyncio.run(client.start(TOKEN))