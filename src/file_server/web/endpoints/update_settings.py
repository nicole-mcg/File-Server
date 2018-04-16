from file_server.web.endpoint import Endpoint

from file_server.account.account_manager import update_settings

# This class is used to handle requests for updating user settings
class UpdateSettingsEndpoint(Endpoint):
    PATH = "updatesettings"

    # Handles a request from the HTTP server for the endpoint
    # See Endpoint.handle_request for argument documentation
    def handle_request(self, request_handler, server, account, data):

        # Verify we've got a dict as data before passing
        if not isinstance(data, dict):
            return {"error": "Invalid request format"}

        # Attempt to update the account with the specified settings
        # It's safe to pass the data directly to update_settings because invalid keys are removed
        update_settings(account, data)

        # Return the accounts new settings for verification
        return account.settings