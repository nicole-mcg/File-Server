

class Endpoint:

    def __init__(self):
        self.needs_auth = True

    def handle_request(self, request_handler, server, account, data):
        return None