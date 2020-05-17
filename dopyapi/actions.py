from .resource import Resource
from .regions import Region

class Action(Resource):
    """
    A class used to manage actions in DigitalOcean.

    This is a general class that can used with all types of actions
    it is used when getting information about actions.

    Attributes:
        id (int): A unique identifier for the action
        status (str): The status of the action it could be "in-progress", "completed" and "errored"
        type (str): The type of action, for example "transfer" to represent the state of image
            transfer action.
        started_at (datetime): The time when the action started
        completed_at (datetime): The time when the action was completed.
        resource_id (int): The unique identifier for the resource associated with this action
        resource_type (str): The type of resource associated with this action
        region (Region): The region where the action occured.
        region_slug (str): The region slug where the action occured.
    """
    _url = "actions"
    """
    The API endpoint for actions
    """
    _single = "action"
    """
    The dictionary index used when fetching a single instance
    """
    _plural = "actions"
    """
    The dictionary index used when fetching multiple instances
    """
    _fetch_attrs = ["id"]
    """
    The attributes used when fetching instances from DigitalOcean
    """
    _dynamic_attrs = []
    """
    The attributes used when creating actions.
    """
    _static_attrs = ["status", "type", "started_at", "completed_at", "resource_id", "resource_type", "region", "region_slug"]
    """
    The attributes filled by DigitalOcean and cannot be changed directly
    """
    _action_attrs = []
    """
    The defined actions
    """
    _update_attr = ""
    """
    The attribute used when updating an action
    """
    _delete_attr = ""
    """
    The attribute used when deleting an action
    """
    _action_attr = ""
    """
    The attribute used when calling actions
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "action"
    def __init__(self, data=None):
        super().__init__(Action)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Action id: {self.id}, status: {self.status}>"
    @classmethod
    def list(cls, **kwargs):
        """
        Used to get a list of all actions

        Args:
            per_page (int): The number of actions returned in a single page result (defaults to 20)
            page (int): The page to be fetched from DigitalOcean (defaults to 1)

        Returns:
            list: A list of actions objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        actions = super().list(**kwargs)
        return [cls(x) for x in actions]
