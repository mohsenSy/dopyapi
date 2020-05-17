import time

from .resource import Resource
from .snapshots import Snapshot
from .actions import Action
from .sizes import Size
from .regions import Region
from .images import Image

class Droplet(Resource):
    """
    This class represents a single Droplet in Digital Ocean

    You can use this class to create, update, delete and manage droplets
    on your Digital Ocean account, all droplet actions are available
    as instance methods and droplet attributes are available too.

    Attributes:
        id (int): A unique identifier for the droplet, it is generated
            when the droplet is created.
        name (str): A human readable name for the droplet
        memory (int): memory of the droplet in megabytes
        vcpus (int): The number of virtual CPUs.
        disk (int): The size of droplet disk in megabytes.
        locked (bool): A boolean value that tells if the droplet is locked
            preventing actions by users.
        created_at (datetime.datetime): A time object that tells when the droplet
            was created.
        status: (str): A status string indicating the state of the droplet, it could
            be ("new", "active", "off", "archive").
        backup_ids (list): An array of backup IDs that have been created for the droplet.
        snapshot_ids (list): An array of snapshot IDs that have been created for the droplet.
        features (list): An array of features enabled for the droplet.
        region (Region): A value for the region where the droplet was created.
        image (Image): A value for the base image used to create the droplet
        size (Size): A value for the size object used to create the droplet, this
            defines the amount of RAM, VCPUS and disk available for the droplet.
        size_slug (str): A unique slug identifier for the size of this droplet.
        networks (dict): An object that defines all networks connected to the droplet
            it includes a key of "IPv4" and "IPv6" if enabled, each key has an array
            of objects that contain network related information such as IP address, netmask
            and gateway plus more information specific for the network type.
        kernel (dict): The current kernel for the droplet.
        next_backup_window (dict): If backups are enabled for the droplet here we will
            find an object with keys to the start and end times for the backups.
        tags (list): An array of tags used when the droplet was created.
        volume_ids (list): An array of block storage volumes attached to the droplet.
        vpc_uuid (str): A string specifying the UUID of the VPC to which the Droplet is assigned.
    Supported actions:
        You can call these actions as methods on :class:`~dopyapi.droplets.Droplet` objects
        and return :class:`~dopyapi.actions.Action` objects

        enable_backups: Used to enable backups for the droplet

        disable_backups: Used to disable backups for the droplet

        reboot: used to reboot the droplet

        power_cycle: Power cycle the droplet

        shutdown: Attempt a gracefull shutdown of the droplet

        power_off: hard shutdown of the droplet

        power_on: power the droplet back on

        restore: Restore this droplet to a previous backup, this takes an ``image`` arg and it should be the ID of a backup for current droplet.

        password_reset: Request a password reset for the droplet.

        resize: Resize the droplet for a new size, this takes ``size`` arg it should be the slug identifier for a size, and also a ``disk`` arg that can be True or False based on whether you want to resize disk as well or not.

        rebuild: Rebuild this droplet with a new image, it takes ``image`` arg for the image that the droplet will use as new base image.

        rename: Chnage the name of the droplet, it takes ``name`` arg.

        change_kernel: Change the kernel of this droplet, it takes ``kernel`` arg which is the unique number of the new kernel to use.

        enable_ipv6: Enable IPv6 for the droplet.

        enable_private_networking: Enable private networking for the droplet.

        snapshot: Take a snapshot for the droplet, it takes ``name`` arg.

    """
    _url = "droplets"
    """
    The URL used for the droplets endpoint
    """
    _plural = "droplets"
    """
    The dictionary key used when fetching multiple droplets
    """
    _single = "droplet"
    """
    The dictionary key used when fetching a single droplet
    """
    _fetch_attrs = ["id", "name"]
    """
    These attributes can be used to fetch a droplet by their value
    """
    _static_attrs = ["memory", "vcpus", "disk", "locked", "created_at", "status", "backup_ids", "snapshot_ids", "features", "region", "image", "size", "size_slug", "networks", "kernel", "next_backup_window", "volume_ids"]
    """
    These attributes are set by Digital Ocean for a droplet and cannot be changed directly
    """
    _dynamic_attrs = ["name", "region", "size", "image", "ssh_keys", "backups", "ipv6", "private_networking", "user_data", "monitoring", "volumes", "tags", "vpc_uuid"]
    """
    These attributes can be used when creating a new droplet or updating an existing one
    """
    _action_attrs = ["enable_backups", "disable_backups", "power_cycle", "reboot", "shutdown", "power_off", "power_on", "restore", "password_reset", "resize", "rebuild", "rename", "change_kernel", "enable_ipv6", "enable_private_networking", "snapshot"]
    """
    These are the actions that can be used with the droplet, each one is a function that return :class:`~dopyapi.actions.Action` object

            enable_backups: Used to enable backups for the droplet

            disable_backups: Used to disable backups for the droplet

            reboot: used to reboot the droplet

            power_cycle: Power cycle the droplet

            shutdown: Attempt a gracefull shutdown of the droplet

            power_off: hard shutdown of the droplet

            power_on: power the droplet back on

            restore: Restore this droplet to a previous backup, this takes an ``image`` arg and it should be the ID of a backup for current droplet.

            password_reset: Request a password reset for the droplet.

            resize: Resize the droplet for a new size, this takes `size` arg
                it should be the slug identifier for a size, and also a `disk` arg
                that can be True or False based on whether you want to resize disk
                as well or not.

            rebuild: Rebuild this droplet with a new image, it takes `image` arg
                for the image that the droplet will use as new base image.

            rename: Chnage the name of the droplet, it takes `name` arg.

            change_kernel: Change the kernel of this droplet, it takes `kernel`
                arg which is the unique number of the new kernel to use.

            enable_ipv6: Enable IPv6 for the droplet.

            enable_private_networking: Enable private networking for the droplet.

            snapshot: Take a snapshot for the droplet, it takes `name` arg.
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete droplets by its value
    """
    _update_attr = ""
    """
    This is the name of the attribute used to update droplets by its value
    """
    _action_attr = "id"
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "droplet"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(Droplet)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Droplet name: {self.name}>"
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of droplets as defined by its arguments

        Arguments:
            page (int): The page to fetch from all droplets (defaults 1)
            per_page (int): The number of droplets per a single page (defaults 20)

        Returns:
            list: A list of droplets
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        droplets = super().list(**kwargs)
        return [cls(x) for x in droplets]
    @classmethod
    def listByTagName(cls, tag_name, **kwargs):
        """
        This method returns a list of droplets that match the tag name

        Arguments:
            tag_name (str): The tag used when fetching droplets
            page (int): The page to fetch from all droplets (defaults 1)
            per_page (int): The number of droplets per a single page (defaults 20)

        Returns:
            list: A list of droplets
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(url=f"{cls._url}", tag_name=tag_name, **kwargs)
    def listKernels(self, **kwargs):
        """
        Return a list of kernels that can be used with this droplet

        Arguments:
            page (int): The page of kernels to return
            per_page (int): The number of kernels per a single page (defaults 20)
        Returns:
            list: A list of kernels, where each kernel is a dict
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return self.list(url=f"{self._url}/{self.id}/kernels", index="kernels", **kwargs)
    def listSnapshots(self, **kwargs):
        """
        Return a list of snapshots for this droplet

        Arguments:
            page (int): The page of snapshots to return
            per_page (int): The number of snapshots per a single page (defaults 20)
        Returns:
            list: A list of snapshots
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        snapshots = super().list(url=f"{self._url}/{self.id}/snapshots", index="snapshots", **kwargs)
        return [Image(x) for x in snapshots]
    def listBackups(self, **kwargs):
        """
        Return a list of backups for this droplet

        Arguments:
            page (int): The page of backups to return
            per_page (int): The number of backups per a single page (defaults 20)
        Returns:
            list: A list of backups, where each one is a dict
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return self.list(url=f"{self._url}/{self.id}/backups", index="backups", **kwargs)
    def listNeighbors(self, **kwargs):
        """
        This method returns a list of droplets that are on the same physical server as this one

        Arguments:
            page (int): The page to fetch from all droplets (defaults 1)
            per_page (int): The number of droplets per a single page (defaults 20)

        Returns:
            list: A list of droplets
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return self.list(url=f"{self._url}/{self.id}/neighbors", index="droplets", **kwargs)
    @classmethod
    def deleteByTagName(cls, tag_name):
        """
        Delete all droplets whose tag_name equals `tag_name`

        Arguments:
            tag_name (str): The name of the tag to delete droplets that match it
        Return:
            dict : A dictionary with one key "status" and value "deleted".

        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        return cls().delete(url="droplets", tag_name=tag_name)
    @classmethod
    def actionByTagName(cls, tag_name, action, **kwargs):
        """
        Execute the action on all droplets with a specific tag.

        Args:
            tag_name (str): The name of tag to use.
            action (str): The name of the action.
        Return:
            Action: This object represents the action used.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls().__getattribute__(action)(url="droplets/actions", tag_name=tag_name, **kwargs)
    @classmethod
    def listDropletNeighbors(cls):
        """
        This method returns a list of droplets that are on the same physical server.

        The return value will be a list of lists.

        Returns:
            list: A list of droplets IDs
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return super().list(url="reports/droplet_neighbors_ids", index="neighbor_ids")
    def waitReady(self):
        """
        Wait until a droplet is ready and running
        """
        while True:
            if self.status == "active" or self.status == "off":
                return
            time.sleep(self.ttl)
            self.load()

    def getPublicIP(self):
        """
        Retrieve the public IP address of the droplet

        This method makes sure that the droplet is active
        and returns its IP address as a string

        Returns:
            str: The public IP address
        """
        self.waitReady()
        networks_ipv4 = self.networks["v4"]
        for network in networks_ipv4:
            if network["type"] == "public":
                return network["ip_address"]
    def getPrivateIP(self):
        """
        Retrieve the private IP address of the droplet if available

        This method makes sure that the droplet is active
        and returns its IP address as a string, if not available
        return None

        Returns:
            str: The private IP address or None if not available
        """
        self.waitReady()
        networks_ipv4 = self.networks["v4"]
        for network in networks_ipv4:
            if network["type"] == "private":
                return network["ip_address"]
    def getPublicIPv6(self):
        """
        Retrieve the public v6 IP address of the droplet if available

        This method makes sure that the droplet is active
        and returns its IP address as a string, if not available
        return None

        Returns:
            str: The public IP v6 address or None if not available
        """
        self.waitReady()
        try:
            return self.networks["v6"][0]["ip_address"]
        except IndexError:
            pass
