from .resource import Resource
from .regions import Region
from .droplets import Droplet
from .actions import Action

class FloatingIP(Resource):
    """
    This class represents a single Floating IP in Digital Ocean

    You can use this class to create, update, delete and manage floating IPs
    on your Digital Ocean account, all floating IP actions are available
    as instance methods and floating IP attributes are available too.

    Attributes:
        ip (str): The public IP address of the floating IP. It also serves as its identifier.
        region (Region): The region that the floating IP is reserved to.
        droplet (Droplet): The Droplet that the floating IP has been assigned to.

    Supported actions:
        You call these actions as methods on :class:`~dopyapi.floating_ips.FloatingIP`
        and return :class:`~dopyapi.actions.Action` objects

        assign: Used to assign the floating IP to a droplet, it takes a single argument ``droplet_id`` which is the ID of droplet or a :class:`~dopyapi.droplets.Droplet` object.

        unassign: Used to remove a floating IP from a droplet.
    """
    _url = "floating_ips"
    """
    The URL used for the Floating IP endpoint
    """
    _plural = "floating_ips"
    """
    The dictionary key used when fetching multiple Floating IPs
    """
    _single = "floating_ip"
    """
    The dictionary key used when fetching a single Floating IP.
    """
    _fetch_attrs = ["ip"]
    """
    These attributes can be used to fetch a Floating IP by their value
    """
    _dynamic_attrs = ["region", "droplet"]
    """
    These attributes can be used when creating a new Floating IP or updating an existing one
    """
    _static_attrs = []
    """
    These attributes are set by Digital Ocean for a Floating IP and cannot be changed directly
    """
    _action_attrs = ["assign", "unassign"]
    """
    These are the actions that can be used with the Floating Ip, each one is a function that return action object
    """
    _delete_attr = "ip"
    """
    This is the name of the attribute used to delete Floating IPs by its value
    """
    _update_attr = ""
    """
    This is the name of the attribute used to update Floating IPs by its value
    """
    _action_attr = "ip"
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "ip"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "floating_ip"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(FloatingIP)
        if data is not None:
            self._update({self._single: data})
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of Floating IPs as defined by its arguments

        Arguments:
            page (int): The page to fetch from all Floating IPs (defaults 1)
            per_page (int): The number of Floating IPs per a single page (defaults 20)

        Returns:
            list: A list of Floating IPs
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        fps = super().list(**kwargs)
        ret = []
        for fp in fps:
            ret.append(cls(fp))
        return ret
    def __repr__(self):
        return f"<FloatingIP ip: {self.ip}, region: {self.region}>"
