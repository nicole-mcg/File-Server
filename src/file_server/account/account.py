# This class represents an account loaded from the server
# This can be used in the client
class Account:
    
    # The default settings for new accounts
    DEFAULT_SETTINGS = {
        "refresh_rate": 0
    }

    # name: the name (usename) for the account
    # auth_code: the authorization code used to create this account
    # settings: the current settings for the account, any settings not specified will be filled in by DEFAULT_SETTINGS
    def __init__(self, name, auth_code, settings):
        self.name = name.title()
        self.auth_code = auth_code
        self._settings = settings

    # The full list of settings for the account
    @property
    def settings(self):
        return dict(Account.DEFAULT_SETTINGS, **self._settings)

    # Used to check if two objects reference the same account
    # account1 == account2
    def __eq__(self, other):
        return other.name == self.name and other.auth_code == self.auth_code