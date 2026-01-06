import requests

class RequestHandler:
    def __init__(self):
        self.headers = {}
        self.base_url = "https://api.stoat.chat"
        
    def update_headers(self, bot_token: str):
        if not bot_token:
            return
        
        self.headers = {
            "X-Bot-Token": bot_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "StoatPyClient/1.0"
        }
    
    def send_request(self, endpoint: str, method: str, data=None, **kwargs):
        kwargs.setdefault('headers', self.headers)
        url = self.base_url + endpoint
        if data is not None and isinstance(data, dict):
            response = requests.request(method, url, json=data, **kwargs)
        else:
            response = requests.request(method, url, data=data, **kwargs)
        return response

req = RequestHandler()