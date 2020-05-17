from .resource import Resource

class Snapshot(Resource):
    """
    This class represents snapshots in Digital Ocean.

    Each snapshot is a saved image from a droplet or a block storage
    volume, the resource_type attribute defines if the snapshot is
    for a droplet or volume.

    Attributes:
        id (str): The unique identifier for the snapshot.
        name (str): A human-readable name for the snapshot.
        created_at (datetime): The date where the snapshot was created.
        regions (list): A list of region slugs that the image is available in.
        resource_id (str): A unique identifier for the resource that the snapshot is associated with.
        resource_type (str): The type of resource for this snapshot.
        min_disk_size (int): The minimum size in GB required for a volume or droplet
            to use this snapshot.
        size_gigabytes (float): The size of snapshot.
        tags (list): A list of tags for the snapshot.
    """
    _url = "snapshots"
    """
    The API endpoint for snapshots.
    """
    _single = "snapshot"
    """
    The dictionary index used when fetching single snapshot instance.
    """
    _plural = "snapshots"
    """
    The dictionary index used when fetching multiple snapshot instances.
    """
    _fetch_attrs = ["id"]
    """
    The attributes that can be used to fetch snapshot instances.
    """
    _dynamic_attrs = []
    """
    The attribute that can be changed on snapshots.
    """
    _static_attrs = ["name", "created_at", "regions", "resource_id", "resource_type", "min_disk_size", "size_gigabytes", "tags"]
    """
    Snapshot attributes that cannot be changed.
    """
    _action_attrs = []
    """
    List of snapshot defined actions.
    """
    _delete_attr = "id"
    """
    The attribute used when deleting a snapshot.
    """
    _update_attr = ""
    """
    The attribute used when updating a snapshot.
    """
    _id_attr = "id"
    """
    The name of attribute used as an ID for snapshots.
    """
    _action_attr = ""
    """
    The attribute used when calling actions.
    """
    def __init__(self, data=None):
        super().__init__(Snapshot)
        if data is not None:
            print(f"data is {data}")
            self._update({self._single: data})
    def __repr__(self):
        return f"<Snapshot name: {self.name}>"
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of snapshot instances.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)

        Return:
            list : A list of snapshot instances.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        snapshots = super().list(**kwargs)
        ret = []
        for snapshot in snapshots:
            ret.append(cls(snapshot))
        return ret
    @classmethod
    def listDropletSnapshots(cls, **kwargs):
        """
        Return a list of droplet snapshots.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)

        Return:
            list : A list of droplet snapshots.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(resource_type="droplet")
    @classmethod
    def listVolumeSnapshots(cls, **kwargs):
        """
        Return a list of volume snapshots.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)

        Return:
            list : A list of volume snapshots.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(resource_type="volume")
