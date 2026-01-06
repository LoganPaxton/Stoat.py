from stoat_py.classes import Channel, Client, Message

client = Client()
client.login("") # No token for public (I see you)

""" channel = Channel()
members = channel.createWebhook("01KE7HCF6VZACAWNEJVADFZJD0", {'name': 'Test', 'avatar': '00000000000000'}) """
msg = Message()
res = msg.sendMessage("01KE7FGF0ENHN49SQVPN3WVGVK", "Hello, World!")
print(res)