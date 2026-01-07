class AuthenticationError(Exception):
    def __init__(self, message="There was an error whilst attempting to authenticate."):
        self.message = message
        super().__init__(self.message)