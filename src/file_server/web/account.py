
import json, os, random
import uuid

from passlib.hash import sha512_crypt
from time import time

#This class is available for use in Client simply for data purposes
#Methods should not be used in the client
class Account:
    TWO_DAYS = 172800
    sessions = {}

    def end_session(session):
        if session in Account.sessions.keys():
            del Account.sessions[session]

    def create_auth():
        auth_code = uuid.uuid4().hex

        directory = "../bin/"
        file_name = directory + "auths.json"

        existing_auths = {}
        if os.path.isfile(file_name):

            file = open(file_name, "r")
            contents = file.read()
            file.close()

            existing_auths = json.loads(contents)

        existing_auths[auth_code] = time() + Account.TWO_DAYS

        os.makedirs(directory, exist_ok=True)
        file = open(file_name, "w")
        file.write(json.dumps(existing_auths))
        file.close()

        return auth_code

    def is_valid_session(session):
        return session in Account.sessions

    def is_valid_auth(auth_code):
        directory = "../bin/"
        file_name = directory + "auths.json"

        existing_auths = {}
        if not os.path.isfile(file_name):
            return False

        file = open(file_name, "r")
        contents = file.read()
        file.close()

        existing_auths = json.loads(contents)

        print(auth_code)
        print(existing_auths)

        if auth_code in existing_auths.keys():

            if existing_auths[auth_code] > time():
                del existing_auths[auth_code]
                file = open(file_name, "w")
                file.write(json.dumps(existing_auths))
                file.close()
                return True 

        return False

    def _create_session(account):
        id = uuid.uuid4().hex
        Account.sessions[id] = account
        account.session = id
        return account

    def load_account(session):
        return sessions[session]

    def load_account(name, password):
        name = name.lower()

        file_name = "../bin/accounts/" + name + ".json"

        if not os.path.isfile(file_name):
            return None

        file = open(file_name, "r")
        contents = file.read()
        file.close()

        data = json.loads(contents)

        if sha512_crypt.verify(password, data["password"]) == False:
            return None

        print(data)

        return Account._create_session(Account(name, data["auth_code"], data["settings"]))


    def create_account(name, password, auth_code):
        file_name = "../bin/accounts/" + name + ".json"

        if os.path.isfile(file_name):
            return None

        if not Account.is_valid_auth(auth_code):
            print("invalid auth")
            return None

        settings = {
            "refresh_rate": 0,
        }

        account = Account(name, auth_code, settings)

        

        os.makedirs("../bin/accounts/", exist_ok=True)
        file = open(file_name, "w")
        file.write(json.dumps({
            "password": sha512_crypt.hash(password),
            "auth_code": auth_code,
            "settings": settings,
        }))
        file.close()

        return Account._create_session(Account(name, auth_code, settings))

    def save_settings(account):
        file_name = "../bin/accounts/" + account.name.lower() + ".json"

        os.makedirs("../bin/accounts/", exist_ok=True)

        if not os.path.isfile(file_name):
            raise Exception("WTF")

        file = open(file_name, "r")
        contents = file.read()
        file.close()

        data = json.loads(contents)

        file = open(file_name, "w")
        file.write(json.dumps({
            "password": data["password"],
            "auth_code": data["auth_code"],
            "settings": account.settings,
        }))
        file.close()

    def __init__(self, name, auth_code, settings):
        self.name = name.title()
        self.auth_code = auth_code
        self.settings = settings