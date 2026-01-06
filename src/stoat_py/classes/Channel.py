from stoat_py.utils.request_handler import req

class Channel:
    def __init__(self):
        pass
    
    def getMembers(self, channel_id: str):
        request = req.send_request(f"/channels/{channel_id}/members", "GET")
        return request.json()
    
    def createWebhook(self, channel_id: str, data: dict):
        request = req.send_request(f"/channels/{channel_id}/webhooks", "POST", data)
        return request.json()