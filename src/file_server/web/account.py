
import json, os, random
import uuid

from passlib.hash import sha512_crypt
from time import time

#This class is available for use in Client simply for data purposes
#Methods should not be used in the client
class Account:
    TWO_DAYS = 172800
    sessions = {}

    #This can be changed in tests to avoid changing or loading real accounts
    #To get current python file directory:
    #   import os, inspect
    #   curr_path = os.path.split(inspect.stack()[0][1])[0]
    directory = "../bin/" 
    

    def end_session(session):
        if session in Account.sessions.keys():
            del Account.sessions[session]

    def create_auth():
        auth_code = uuid.uuid4().hex

        directory = Account.directory
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
        directory = Account.directory

        if auth_code == "" and (not os.path.isdir("{}accounts/".format(directory)) or len(os.listdir("{}accounts/".format(directory))) == 0):
            return True

        file_name = directory + "auths.json"

        existing_auths = {}
        if not os.path.isfile(file_name):
            return False

        file = open(file_name, "r")
        contents = file.read()
        file.close()

        existing_auths = json.loads(contents)

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

        file_name = Account.directory + "accounts/" + name + ".json"

        if not os.path.isfile(file_name):
            return None

        file = open(file_name, "r")
        contents = file.read()
        file.close()

        data = json.loads(contents)

        if sha512_crypt.verify(password, data["password"]) == False:
            return None

        return Account._create_session(Account(name, data["auth_code"], data["settings"]))


    def create_account(name, password, auth_code):
        directory = Account.directory

        file_name = directory + "accounts/" + name + ".json"

        if os.path.isfile(file_name):
            return None

        if not Account.is_valid_auth(auth_code):
            print("invalid auth")
            return None

        if auth_code == "":
            auth_code = create_auth()

        settings = {
            "refresh_rate": 0,
        }

        account = Account(name, auth_code, settings)

        os.makedirs(directory + "accounts/", exist_ok=True)
        file = open(file_name, "w")
        file.write(json.dumps({
            "password": sha512_crypt.hash(password),
            "auth_code": auth_code,
            "settings": settings,
        }))
        file.close()

        return Account._create_session(Account(name, auth_code, settings))

    def save_settings(account):
        directory = Account.directory
        file_name = directory + "accounts/" + account.name.lower() + ".json"

        os.makedirs(directory + "accounts/", exist_ok=True)

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

    def __eq__(self, other):
        return other.name == self.name and other.auth_code == self.auth_code