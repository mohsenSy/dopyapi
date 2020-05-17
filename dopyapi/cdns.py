from .resource import Resource

class CDN(Resource):
    """
    This class represents CDN endpoints in Digital Ocean

    Here we can create, list, update and delete CDN Endpoints
    which are used to serve static content from Digital Ocean Spaces
    to users all around the world.

    Attributes:
        id (str): A unique ID that can be used to identify and reference a CDN endpoint.
        origin (str): The fully qualified domain name (FQDN) for the origin server which
            provides the content for the CDN. This is currently restricted to a Space.
        endpoint (str): The fully qualified domain name (FQDN) from which the CDN-backed content is served.
        created_at (str): The time when the CDN Endpoint was created.
        ttl (int): The amount of time the content is cached by the CDN's edge servers in seconds.
        certificate_id (str): The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.
        custom_domain (str): The fully qualified domain name (FQDN) of the custom subdomain used with the CDN Endpoint.
    """
    _url = "cdn/endpoints"
    """
    The URL used for the CDN endpoint
    """
    _plural = "endpoints"
    """
    The dictionary key used when fetching multiple CDN Endpoints
    """
    _single = "endpoint"
    """
    The dictionary key used when fetching a single CDN Endpoint
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a CDN Endpoint by their value
    """
    _static_attrs = ["endpoint", "created_at"]
    """
    These attributes are set by Digital Ocean for a CDN Endpoint and cannot be changed directly
    """
    _dynamic_attrs = ["origin", "ttl", "certificate_id", "custom_domain"]
    """
    These attributes can be used when creating a new CDN Endpoint or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the CDN Endpoint, each one is a function that return action object
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete CDN Endpoints by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update CDN Endpoints by its value
    """
    _action_attr = "id"
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "endpoint"
    """
    This holds the type of resource.
    """
    def __init__(self, data = None):
        super().__init__(CDN)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<CDN id:{self.id}, endpoint:{self.endpoint}>"
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of CDN Endpoints as defined by its arguments

        Arguments:
            page (int): The page to fetch from all CDN Endpoints (defaults 1)
            per_page (int): The number of CDN Endpoints per a single page (defaults 20)

        Returns:
            list: A list of CDN Endpoints
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        endpoints = super().list(**kwargs)
        return [cls(x) for x in endpoints]
