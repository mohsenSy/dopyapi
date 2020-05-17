import os

class Auth:
    """
    This class holds authentication information

    Here we store the authentication information needed by other classes
    to access and authenticate to Digital Ocean API, these information are
    stored in attributes as shown below

    Attributes:
        token (str): The authentication token for the Digital Ocean API.
        base_url (str): The base URL used for all API calls. Defaults (https://api.digitalocean.com/v2)

    raises:
        AuthenticationNeeded: This is raised in case no token is provided and
                it cannot be found in "DO_TOKEN" environment variable.
    """
    def __init__(self, token = None, base_url="https://api.digitalocean.com/v2"):
        if token is None:
            try:
                token = os.environ["DO_TOKEN"]
            except KeyError:
                raise AuthenticationNeeded()
        self.token = token
        self.base_url = base_url

def authenticate(token=None, base_url="https://api.digitalocean.com/v2"):
    """
    Store authentication information for the Resource class

    The Resource class is base for all Digital Ocean resources, this function
    creates a new authentication object from the data provided in arguments
    and assigns it to the Resource class as class attribute

    Args:
        token (str): The token used to authenticate to Digital Ocean API. defaults (None)
        base_url (str): The URL used for all API calls. defaults (https://api.digitalocean.com/v2)

    raises:
        AuthenticationNeeded: This is raised in case no token is provided and
            it cannot be found in "DO_TOKEN" environment variable.
    """
    auth_obj = Auth(token, base_url)
    from .resource import Resource
    Resource.auth = auth_obj
    return auth_obj

class AuthenticationNeeded(Exception):
    """
    This exception is raised when no authentication data is provided.
    """
