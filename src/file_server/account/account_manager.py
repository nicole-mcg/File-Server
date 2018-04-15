import json, os, time, uuid
from passlib.hash import sha512_crypt

from file_server.account.account import Account

# This file holds function for accounts used by the server

# Two days in seconds
TWO_DAYS = 172800

#This can be changed in tests to avoid changing or loading real accounts
#To get current python file directory:
#   import os, inspect
#   curr_path = os.path.split(inspect.stack()[0][1])[0]
directory = "../bin/"
sessions = {}

# Changes the directory to hold account information
# new_directory: the new account directory
def set_account_manager_directory(new_directory):

    # Use global because we are changing a global variable
    global directory

    directory = new_directory

# Ends a session with the server
# session: the session to end
def end_session(session):
    if session in sessions.keys():
        del sessions[session]

# Creates a new authorization code for signup
def create_signup_auth():

    file_name = directory + "auths.json"

    # Gnerate a new auth code
    auth_code = uuid.uuid4().hex

    # Load existing auths from file
    # This is so that we can rewrite them into the new file
    existing_auths = {}
    if os.path.isfile(file_name):

        # Load contents of file into existing_auths
        file = open(file_name, "r")
        contents = file.read()
        file.close()
        existing_auths = json.loads(contents)

    # Add the new auth to the existing_auths dict
    # Set expiry time for two days from now
    existing_auths[auth_code] = time.time() + TWO_DAYS

    # Create directory for account information if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Write the new data into the auths file
    file = open(file_name, "w")
    file.write(json.dumps(existing_auths))
    file.close()

    return auth_code

# Checks if a session with the server is valid
# session: the session code to check
def is_valid_session(session):
    return session in sessions

# Checks if a signup authorization code is valid
# auth_code: the authorization code to check
# invalidate_auth: if true, the auth_code is removed from the valid auths file
def is_valid_signup_auth(auth_code, invalidate_auth=False):

    # If there are no accounts created yet then signup doesn't require an auth code (i.e any code inputted is valid)
    if auth_code == "" and (not os.path.isdir("{}accounts/".format(directory)) or len(os.listdir("{}accounts/".format(directory))) == 0):
        return True

    file_name = directory + "auths.json"

    # Return false if there are no auths currently generated
    if not os.path.isfile(file_name):
        return False

    # Load existing auth codes
    file = open(file_name, "r")
    contents = file.read()
    file.close()
    existing_auths = json.loads(contents)

    # Check if we've got a matching auth code that isn't expired
    if auth_code in existing_auths.keys() and existing_auths[auth_code] > time.time():

        # Rewrite the auths file without this auth
        if invalidate_auth:
            del existing_auths[auth_code]
            file = open(file_name, "w")
            file.write(json.dumps(existing_auths))
            file.close()

        return True 

    # We didn't find a matching auth
    return False

# Loads an account from current server sessions
def load_account_from_session(session):
    return sessions[session]

# Loads an account from the current account manager directory
# name: the name (username) for the account
# password: the password for the account
def load_account(name, password):
    name = name.lower()

    file_name = directory + "accounts/" + name + ".json"

    # Account file doesn't exist
    if not os.path.isfile(file_name):
        return None

    # Load account file
    file = open(file_name, "r")
    contents = file.read()
    file.close()
    data = json.loads(contents)

    # Verify password is correct
    if sha512_crypt.verify(password, data["password"]) == False:
        return None

    return _create_session(Account(name, data["auth_code"], data["settings"]))

# Creates a new account using the specified credentials
# This function will still succeed if no auth_code is specified (auth_code="")
# name: the name (username) for the account
# password: the password for the account
# auth_code: the auth code used to create the account
def create_account(name, password, auth_code):
    file_name = directory + "accounts/" + name + ".json"

    # The account file already exists
    if os.path.isfile(file_name):
        return None

    # Generate an auth code if one isn't provided
    if auth_code == "":
        auth_code = create_signup_auth()

    # Make sure the auth is valid if it was provided
    # This is also use up the auth if it was generated above
    if not is_valid_signup_auth(auth_code, True):
        print("invalid auth")
        return None

    # Create the directory for account information if it doesn't exist
    os.makedirs(directory + "accounts/", exist_ok=True)

    # Create account file and write information
    file = open(file_name, "w")
    file.write(json.dumps({
        "password": sha512_crypt.hash(password),
        "auth_code": auth_code,
        "settings": {},
    }))
    file.close()

    return _create_session(Account(name, auth_code, {}))

# Updates the settings with the specified account
# account: the account object to update the settings for
# settings: a dict of the new settings. See Account.DEFAULT_SETTINGS for information
#           not all settings need to be provided here, and incorrect settings will be silently removed
def update_settings(account, settings):
    file_name = directory + "accounts/" + account.name.lower() + ".json"

    # FIXME this exception should be a little more specific
    #       a custom class should be created for different account exceptions
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

    # Update the settings in the account object
    account._settings = settings

# Used to easily create a new session for created accounts
# Returns the account object so it can be chained or returned
# leading underscore indicates a private variable
def _create_session(account):

    # Generate a session code
    id = uuid.uuid4().hex

    # Add account to sessions
    sessions[id] = account
    account.session = id

    return account