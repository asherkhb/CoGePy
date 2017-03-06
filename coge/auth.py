import errors

class AuthToken(object):

    def __init__(self, username, token=None, password=None):
        self.username = username

        if password and not token:
            # self.token = self.new_token(username, password)
            print("[CoGe API] %s - ERROR - Password authentication not yet supported. Please specify a token.")
            raise errors.AuthError("Method not supported.")
        elif token:
            self.token = token
        else:
            print("[CoGe API] %s - ERROR - A valid token or user password must be specified to create an AuthToken.")
            raise errors.AuthError("Invalid AuthToken instantiation.")

    def __repr__(self):
        return "< AUTHENTICATION TOKEN >"

    # TODO: Complete these functions...
    @staticmethod
    def new_token(username, password):
        # token = ''
        # return token
        raise NotImplementedError

    def validate_token(self):
        # Check token.
        # Refresh if necessary.
        # Return token.
        raise NotImplementedError

    def refresh_token(self):
        # Refresh a token
        raise NotImplementedError
