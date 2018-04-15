#This class is available for use in FileClient simply for data purposes
#Methods should not be used in the client
class Account:
    
    DEFAULT_SETTINGS = {
        "refresh_rate": 0
    }

    def __init__(self, name, auth_code, settings):
        self.name = name.title()
        self.auth_code = auth_code
        self._settings = settings

    @property
    def settings(self):
        return dict(Account.DEFAULT_SETTINGS, **self._settings)

    def __eq__(self, other):
        return other.name == self.name and other.auth_code == self.auth_code