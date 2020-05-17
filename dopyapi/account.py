import datetime

from .resource import Resource

class Account(Resource):
    """
    Get general information about your account

    This class is used to retrieve information about the user's account,
    these information are saved as instance attributes described below

    Attributes:
        email (str): The email of the user
        uuid (str): A universal unique ID for the user
        droplet_limit (int): The maximum number of droplets this user can create
        floating_ip_limit (int): The maximum number of floating IPs this user can create
        email_verified (bool): This checks if the user has verified their email address
        status (str): The status of user acount
        status_message (str): A string that describes the status of user account
    """
    _fetch_attrs = []
    """
    Attributes that can be used to fetch instances based on them
    """
    _dynamic_attrs = []
    """
    Attributes that can be used to create new instances
    """
    _static_attrs= ["droplet_limit", "email", "uuid", "email_verified", "status", "status_message"]
    """
    Static attributes that are set by DigitalOcean and cannot be changed
    """
    _action_attrs = []
    """
    These are the actions that can be used with the action, each one is a function that return action object
    """
    _delete_attr = ""
    """
    The attribute that can be used to delete instances
    """
    _update_attr = ""
    """
    The attribute that can be used to update instances
    """
    _url = "account"
    """
    The API endpoint for account information
    """
    _single = "account"
    """
    The dictionary index used when fetching single instance
    """
    _plural = "accounts"
    """
    The dictionary index used when fetching instances
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "uuid"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "droplet"
    """
    This holds the type of resource.
    """
    def __init__(self):
        super().__init__(Account)
        account = self.get(self._url)[self._single]
        for attr in self._static_attrs:
            try:
                object.__setattr__(self, attr, account[attr])
            except IndexError:
                pass
    def __repr__(self):
        return f"<Account email: {self.email}>"
