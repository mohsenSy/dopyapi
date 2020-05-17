from .resource import Resource

class VPC(Resource):
    """
    This class is used to manage Virtual Private Clouds (VPCs) in Digital Ocean.

    VPCs allow users to create separate private networks for
        their resources where resources in one VPC cannot
        communicate with resources in another VPC.

    Attributes:
        id (str): A unique ID that can be used to identify and reference the VPC.
        urn (str): The uniform resource name (URN) for the VPC.
        name (str): The name of the VPC. Must be unique and may only contain alphanumeric characters, dashes, and periods.
        region (str): The slug identifier for the region where the VPC will be created.
        ip_range (str): The range of IP addresses in the VPC in CIDR notation.
        description (str): A free-form text field for describing the VPC's purpose. It may be a maximum of 255 characters.
        default (bool): A boolean value indicating whether or not the VPC is the default one for the region.
        created_at (datetime.datetime): A time value given in ISO8601 combined date and time format.
    """
    _url = "vpcs"
    """
    The URL used for the VPC endpoint
    """
    _plural = "vpcs"
    """
    The dictionary key used when fetching multiple VPCs
    """
    _single = "vpc"
    """
    The dictionary key used when fetching a single VPC
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a VPC by their value
    """
    _static_attrs = ["urn", "default", "created_at"]
    """
    These attributes are set by Digital Ocean for a VPC and cannot be changed directly
    """
    _dynamic_attrs = ["name", "region", "ip_range", "description"]
    """
    These attributes can be used when creating a new VPC or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the VPC, each one is a function that return action object
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete VPCs by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update VPCs by its value
    """
    _action_attr = "id"
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "vpc"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(VPC)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<VPC name: {self.name}>"
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of VPCs as defined by its arguments

        Arguments:
            page (int): The page to fetch from all VPCs (defaults 1)
            per_page (int): The number of VPCs per a single page (defaults 20)

        Returns:
            list: A list of VPC objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        vpcs = super().list(**kwargs)
        return [cls(vpc) for vpc in vpcs]
    def listMembers(self):
        """
        Return a list of members with this VPC

        The list contains dictionaries each one with these keys:

        urn: The Uniform Resource Name for the resource used.

        name: The name of resource
        
        created_at: A time value given in ISO8601 combined date and time format that represents when the resource was created.

        Arguments:
            page (int): The page to fetch from all VPCs (defaults 1)
            per_page (int): The number of VPCs per a single page (defaults 20)

        Returns:
            list: A list of dictionaries.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return super().list(url=f"{self._url}/{self.id}/members", index="members")
