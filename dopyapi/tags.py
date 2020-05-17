from .resource import Resource


class Tag(Resource):
    """
    This class represents tags on Digital Ocean.

    A tag is applied on resources and helps to group them
    and facilates lookups and actions on them.

    Attributes:
        name (str): A name for the tag.
        resources (dictionary): An object that contains keys and values
            for all resources tagged with this tag with count and
            last_tagged_uri attribute.
    """
    _url = "tags"
    """
    The API endpoint for tags.
    """
    _single = "tag"
    """
    The dictionary index used when fetching single tag instance.
    """
    _plural = "tags"
    """
    The dictionary index used when fetching multiple tag instances.
    """
    _fetch_attrs = ["name"]
    """
    The attributes that can be used to fetch tag instances.
    """
    _dynamic_attrs = ["name"]
    """
    The attribute that can be changed on tags.
    """
    _static_attrs = ["resources"]
    """
    Tag attributes that cannot be changed.
    """
    _action_attrs = []
    """
    List of snapshot defined actions.
    """
    _delete_attr = "name"
    """
    The attribute used when deleting a tag.
    """
    _update_attr = ""
    """
    The attribute used when updating a tag.
    """
    _action_attr = ""
    """
    The attribute used when calling actions.
    """
    _id_attr = "name"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "tag"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(Tag)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Tag name: {self.name}>"
    def __str__(self):
        return self.name
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of tag instances.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)

        Return:
            list : A list of tag instances.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        tags = super().list(**kwargs)
        ret = []
        for tag in tags:
            ret.append(cls(tag))
        return ret
    def tag(self, resources):
        """
        Tag resources with this tag.

        Args:
            resources: A list of objects that represents Digital Ocean resources.

        Return:
            dict : The response from Digital Ocean API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        data = []
        if not isinstance(resources, list):
            resources = [resources]
        for resource in resources:
            res = {
                "resource_type": resource._resource_type,
                "resource_id": str(resource.__dict__[resource._id_attr])
            }
            data.append(res)
        return self.post(f"{self._url}/{self.name}/resources", {"resources": data})
    def unTag(self, resources):
        """
        remove this tag from resources with.

        Args:
            resources: A list of objects that represents Digital Ocean resources.

        Return:
            dict : An object with key of "status" and value "deleted".
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        data = []
        for resource in resources:
            res = {
                "resource_type": resource._resource_type,
                "resource_id": resource.__dict__[resource._id_attr]
            }
            data.append(res)
        return self.delete(f"{self._url}/{self.name}/resources", {"resources": data})
