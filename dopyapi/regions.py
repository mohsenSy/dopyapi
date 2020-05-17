from .resource import Resource

class Region(Resource):
    """
    This class represents a single region in Digital Ocean

    A region represents a dataceneter where droplets can be created
    and images can be transferred.

    Attributes:
        slug (str): A human readable string that can be used as a unique
            identifier for each region.
        name (str): The display name for the region
        sizes (list): A list of size slugs that are available for this region
        available (bool): A boolean that checks if the region is available or not
        features (list): An array of features available for this region
    """
    _url = "regions"
    """
    The url for the regions endpoint
    """
    _plural = "regions"
    """
    The dictionary index used when fetching multiple regions
    """
    _single = "region"
    """
    The dictionary index used when fetching single region
    """
    _can_fetch = False
    """
    A boolean that tells no single region can be fetched by itself
    """
    _fetch_attrs = []
    """
    A list of attributes that can be used to fetch a single region, empty because
        we cannot fetch single regions
    """
    _dynamic_attrs = []
    """
    A list of attributes that can be used when creating or updating regions, empty
        because we cannot create or update regions
    """
    _static_attrs = ["slug", "name", "sizes", "available", "features"]
    """
    A list of region attributes set by Digital Ocean and cannot be changed
    """
    _action_attrs = []
    """
    A list of actions for the region, empty no actions defined.
    """
    _delete_attr = ""
    """
    An attribute used when deleting a single region, empty because we cannot delete regions
    """
    _update_attr = ""
    """
    An attribute used when updating regions, empty because we cannot update regions
    """
    _action_attr = ""
    """
    An attribute used when calling actions, empty because we cannot call actions
    """
    _resource_type = "region"
    """
    The type of resource
    """
    _id_attr = "slug"
    """
    The attribute used to uniquely identify regions
    """
    def __init__(self, data=None):
        super().__init__(Region)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Region slug: {self.slug}>"
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of regions based on arguments

        Arguments:
            page (int): The page to return
            per_page (int): The number of regions in a single page
        Return:
            list: A list of region objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        regions = super().list(**kwargs)
        return [cls(region) for region in regions]
