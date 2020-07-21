from .resource import Resource

class ClickApp(Resource):
    """
    This class represents 1-Click applications in Digital Ocean.

    These are pre-built Droplet images and kubernetes apps already setup
    for you.

    Attributes:
        slug (str): The slug identifier for the 1-Click application.
        type (str): The type of the 1-Click application, it could be either 'droplet' or 'kubernetes' only so far.
    """
    _url = "1-clicks"
    """
    The URL used for the Click Apps endpoint
    """
    _plural = "1_clicks"
    """
    The dictionary key used when fetching multiple Click Apps.
    """
    _single = "1_click"
    """
    The dictionary key used when fetching a single Click App.
    """
    _fetch_attrs = []
    """
    These attributes can be used to fetch a Click Apps by their value
    """
    _static_attrs = ["slug", "type"]
    """
    These attributes are set by Digital Ocean for a Click App and cannot be changed directly
    """
    _dynamic_attrs = []
    """
    These attributes can be used when creating a new Click App or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the Click Apps, each one is a function that return action object
    """
    _delete_attr = ""
    """
    This is the name of the attribute used to delete Click Apps by its value
    """
    _update_attr = ""
    """
    This is the name of the attribute used to update Click Apps by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "slug"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "clickapps"
    """
    This holds the type of resource.
    """
    def __init__(self, data = None):
        super().__init__(ClickApp)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<ClickApp slug:{self.slug}, type:{self.type}>"
    @classmethod
    def list(cls, type = None):
        """
        This method returns a list of Click Apps as defined by its arguments

        Arguments:
            type (str): The type of Click Apps to list, if None it fetches all click apps. default None

        Returns:
            list: A list of Click Apps
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if type is None:
            clickapps = super().list()
        else:
            clickapps = super().list(type=type)
        return [cls(x) for x in clickapps]
    @classmethod
    def listDroplet(cls):
        """
        This method returns a list of Click Apps of type "droplet"

        Returns:
            list: A list of Click Apps of type droplet only
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        clickapps = super().list(type="droplet")
        return [cls(x) for x in clickapps]
    @classmethod
    def listKubernetes(cls):
        """
        This method returns a list of Click Apps of type kubernetes

        Returns:
            list: A list of Click Apps of type kubernetes
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        clickapps = super().list(type="kubernetes")
        return [cls(x) for x in clickapps]
