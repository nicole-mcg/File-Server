import json, os, time, uuid
from passlib.hash import sha512_crypt

from file_server.account.account import Account

TWO_DAYS = 172800
sessions = {}

#This can be changed in tests to avoid changing or loading real accounts
#To get current python file directory:
#   import os, inspect
#   curr_path = os.path.split(inspect.stack()[0][1])[0]
directory = "../bin/"

def set_account_manager_directory(new_directory):
    global directory

    directory = new_directory

def end_session(session):
    if session in sessions.keys():
        del sessions[session]

def create_signup_auth():
    auth_code = uuid.uuid4().hex
    file_name = directory + "auths.json"

    existing_auths = {}
    if os.path.isfile(file_name):

        file = open(file_name, "r")
        contents = file.read()
        file.close()

        existing_auths = json.loads(contents)

    existing_auths[auth_code] = time.time() + TWO_DAYS

    os.makedirs(directory, exist_ok=True)
    file = open(file_name, "w")
    file.write(json.dumps(existing_auths))
    file.close()

    return auth_code

def is_valid_session(session):
    return session in sessions

def is_valid_signup_auth(auth_code, invalidate_auth=False):
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

    if auth_code in existing_auths.keys() and existing_auths[auth_code] > time.time():
        
        if invalidate_auth:
            del existing_auths[auth_code]
            file = open(file_name, "w")
            file.write(json.dumps(existing_auths))
            file.close()

        return True 

    return False

def load_account_from_session(session):
    return sessions[session]

def load_account(name, password):
    name = name.lower()

    file_name = directory + "accounts/" + name + ".json"

    if not os.path.isfile(file_name):
        return None

    file = open(file_name, "r")
    contents = file.read()
    file.close()

    data = json.loads(contents)

    if sha512_crypt.verify(password, data["password"]) == False:
        return None

    return _create_session(Account(name, data["auth_code"], data["settings"]))

def create_account(name, password, auth_code):
    file_name = directory + "accounts/" + name + ".json"

    if os.path.isfile(file_name):
        return None

    if auth_code == "":
        auth_code = create_signup_auth()

    if not is_valid_signup_auth(auth_code, True):
        print("invalid auth")
        return None

    os.makedirs(directory + "accounts/", exist_ok=True)
    file = open(file_name, "w")
    file.write(json.dumps({
        "password": sha512_crypt.hash(password),
        "auth_code": auth_code,
        "settings": {},
    }))
    file.close()

    return _create_session(Account(name, auth_code, {}))

def update_settings(account, settings):
    file_name = directory + "accounts/" + account.name.lower() + ".json"

    if not os.path.isfile(file_name):
        raise Exception("Tried to update settings on account that was not created through Account.create_account or loaded with Account.load_account")

    # Remove invalid keys
    for key in settings:
        if not key in Account.DEFAULT_SETTINGS:
            del settings[key]

    # Load account data for file rewrite
    file = open(file_name, "r")
    contents = file.read()
    file.close()

    data = json.loads(contents)

    # Rewrite account file with new settings
    file = open(file_name, "w")
    file.write(json.dumps({
        "password": data["password"],
        "auth_code": data["auth_code"],
        "settings": settings,
    }))
    file.close()

    account._settings = settings

# 
# leading underscore indicates a private variable
def _create_session(account):
    id = uuid.uuid4().hex
    sessions[id] = account
    account.session = id
    return account