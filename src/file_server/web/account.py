
import json, os, random
import uuid

#This class is available for use in Client simple for data purposes
#Methods should not be used in the client
class Account:
    sessions = {}

    def create_auth():
        return uuid.uuid4().hex

    def _create_session(account):
        id = uuid.uuid4().hex
        Account.sessions[id] = account
        account.session = id
        return account

    def load_account(session):
        return sessions[session]

    def load_account(name, password):
        file_name = "../bin/accounts/" + name + ".json"

        if not os.path.isfile(file_name):
            return None

        file = open(file_name, "r")
        contents = file.read()
        file.close()

        data = json.loads(contents)

        if password != data["password"]:
            return None

        return Account._create_session(Account(name, data["auth_code"]))

    def create_account(name, password, auth_code):
        file_name = "../bin/accounts/" + name + ".json"

        if os.path.isfile(file_name):
            return None

        os.makedirs("../bin/accounts/", exist_ok=True)
        file = open(file_name, "w")
        file.write(json.dumps({
            "password": password,
            "auth_code": auth_code
        }))
        file.close()

        return Account._create_session(Account(name, auth_code))

    def __init__(self, name, auth_code):
        self.name = name
        self.auth_code = auth_code