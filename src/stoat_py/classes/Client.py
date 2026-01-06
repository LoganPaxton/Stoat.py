from stoat_py.utils.request_handler import req

# API BASE URL: https://api.stoat.chat

class Client:
    def __init__(self):
        self.token = ""
    
    def login(self, token: str) -> None:
        self.token = token
        req.update_headers(token)