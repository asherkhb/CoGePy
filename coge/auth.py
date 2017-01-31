PARAMS = {}


class AuthToken(object):

    def __init__(self, username, password):
        self.username = username
        self.token = self.new_token(username, password)

    def __repr__(self):
        return "< AUTHENTICATION >"

    @staticmethod
    def new_token(username, password):
        token = ''
        return token

    def validate_token(self):
        token = self.token
        # Check token.
        # Refresh if necessary.
        # Return token.
        self.token = token

    def refresh_token(self):
        raise NotImplementedError


def authenticate(func, params):
    """Authentication Decorator

    :param func: Function which can benefit from authentication.
    :return:
    """
    # TODO
    # return func(params=PARAMS)
    raise NotImplementedError
