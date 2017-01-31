import json
from datetime import datetime


class Error(Exception):
    """Base class for module exceptions."""
    pass


class AuthError(Error):
    """Exception raised when authentication is invalid, or fails"""
    def __init__(self, msg):
        self.msg = msg


class InvalidResponseError(Error):
    """Exception raised when a request has an invalid response code."""
    def __init__(self, response):
        self.status_code = response.status_code
        self.msg = json.loads(response.text)['error']['Error']
        # print("%s - ERROR - Invalid response (%d): %s" % (datetime.now(), self.status_code, self.msg))


class InvalidIDError(Error):
    """Exception raised when an ID cannot be converted to an integer"""
    def __init__(self, ids):
        self.ids = ids
