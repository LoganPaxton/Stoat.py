from stoat_py.utils.request_handler import req
import ulid
import time

class Message:
    def __init__(self):
        pass
    
    def sendMessage(self, channel_id: str, msg: str):
        print("[WARNING]: The 'Message' class is now depricated. Please use the channel class.")
        generator = ulid.ULID()
        msg_ulid = generator.from_timestamp(time.time())
        print(str(msg_ulid))
        req.headers['Idempotency-Key'] = str(msg_ulid)
        payload = {
            "content": msg
        }
        req.send_request(f"/channels/{channel_id}/messages", "POST", data=payload)