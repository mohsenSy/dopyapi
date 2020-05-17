from .resource import Resource
from .snapshots import Snapshot
from .regions import Region

class Volume(Resource):
    """
    This class represents a single Block Storage volume in Digital Ocean.

    A volume appears as locally attached disk to a droplet that can be formatted
        by the operating system, it can have sizes from 1GB up to 16TB.

    Attributes:
        id (str): The unique identifier for the Block Storage volume.
        region (Region): The region where the volume is located.
        droplet_ids (list): A list that contains the droplet IDs for droplets
            where this volume is attached to, so far a volume can be attached
            only to a single droplet.
        name (str): A human readable name for the volume.
        description (str): An optional description for the volume.
        size_gigabytes (int): The size of volume in GB.
        created_at (datetime): The time when the volume was created.
        filesystem_type (str): The type of filesystem currently in-use on the volume.
        filesystem_label (str): The label currently applied to the filesystem.
        tags (list): A list of Tags the volume has been tagged with.
    """
    _url = "volumes"
    """
    The API endpoint for volumes.
    """
    _plural = "volumes"
    """
    The dictionary index used when fetching multiple volume instances.
    """
    _single = "volume"
    """
    The dictionary index used when fetching single volume instance.
    """
    _fetch_attrs = ["id"]
    """
    The attributes that can be used to fetch volume instances.
    """
    _dynamic_attrs = ["size_gigabytes", "name", "description", "region", "snapshot_id", "filesystem_label", "filesystem_type", "tags"]
    """
    The attribute that can be changed on volumes.
    """
    _static_attrs = ["droplet_ids", "created_at"]
    """
    Volume attributes that cannot be changed.
    """
    _action_attrs = ["attach", "detach", "resize"]
    """
    List of volume defined actions.
    """
    _delete_attr = "id"
    """
    The attribute used when deleting a volume.
    """
    _update_attr = "id"
    """
    The attribute used when updating a volume.
    """
    _action_attr = "id"
    """
    The attribute used when calling actions.
    """
    _resource_type = "volume"
    """
    The resource type for volumes.
    """
    _id_attr = "id"
    """
    The name of attribute used as an ID for volumes.
    """
    def __init__(self, data=None):
        super().__init__(Volume)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Volume name: {self.name}>"
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of volume instances.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)

        Return:
            list : A list of volume instances.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        volumes = super().list(**kwargs)
        ret = []
        for volume in volumes:
            ret.append(cls(volume))
        return ret
    @classmethod
    def listByName(cls, name, **kwargs):
        """
        Return a list of volume instances by name.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)
            name (str): The pattern for volumes name.

        Return:
            list : A list of volume instances by name.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(name=name, **kwargs)
    def listSnapshots(self, **kwargs):
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
        snapshots = Snapshot.list(url=f"{self._url}/{self.id}/snapshots", index="snapshots", **kwargs)
        return snapshots
    def snapshot(self, name, tags=[]):
        """
        Take a snapshot of a volume.

        This method is used to take a volume snapshot.

        Args:
            name (str): The name of snapshot.
            tags (list): A list of tags for the snapshot (default [])
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        data = {
            "name": name,
            "tags": tags
        }
        resp = self.post(f"{self._url}/{self.id}/snapshots", data)
        return Snapshot(resp["snapshot"])
    @classmethod
    def get_by_name(cls, name, region):
        """
        Get a volume by specifying a region and name

        This method will return a volume with the given name and the used
            region, volumes with the same name could exist in different regions.

        Args:
            name (str): The name of the volume.
            region (str, Region): The name of region or the region object.
        Return:
            Volume: The volume object found
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        vol = cls().get(cls.url, name=name, region=region)
        return Volume(vol["volumes"][0])
    @classmethod
    def delete_by_name(cls, name, region):
        """
        Delete a volume by name and region name

        This method is used to delete a volume by its name and in which
            region it exists.

        Args:
            name (str): The name of the volume.
            region (str, Region): The name of region or the region object.
        Return:
            dict : A dictionary with one key "status" and value "deleted".
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        return cls().delete(url=cls.url, name=name, region=region)
