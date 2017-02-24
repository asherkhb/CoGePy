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
        # Parse response.
        self.status_code = response.status_code
        try:
            self.data = json.loads(response.text)['error']
            self.desc = self.data.keys()[0]
            self.msg = self.data[self.desc]
        except ValueError:
            self.desc = "UNKNOWN RESPONSE"
            self.msg = response.text
        # Print error message.
        self.print_error()

    def print_error(self):
        print("[CoGe API] %s - ERROR - Invalid response (%d, %s): %s" %
              (datetime.now(), self.status_code, self.desc, self.msg))


class InvalidIDError(Error):
    """Exception raised when an ID cannot be converted to an integer"""
    def __init__(self, ids):
        self.ids = ids


class InvalidCogeObject(Error):
    def __init__(self, msg=''):
        self.msg = msg