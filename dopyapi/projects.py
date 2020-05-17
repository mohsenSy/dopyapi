from .resource import Resource

class Project(Resource):
    """
    This class represents a project in Digital Ocean.

    A project allows you to organize your resources in groups that fit
    the applications you run on Digital Ocean.

    Attributes:
        id (str): The unique universal identifier of this project.
        owner_uuid (str): The unique universal identifier of the project owner.
        owner_id (int): The integer id of the project owner.
        name (str): The human-readable name for the project.
        description (str): An optional description text for the project.
        purpose (str): The purpose of the project, it can have one of these
            values ("Just trying out DigitalOcean", "Class project / Educational purposes"
            , "Website or blog", "Web Application", "Service or API", "Mobile Application"
            , "Machine learning / AI / Data processing", "IoT", "Operational / Developer tooling")
            if you use a valume other than these it will be stored as "Other: your custom purpose".
        environment (str): The environment for project resources, it can have one
            of these values ("Development", "Staging", "Production").
        is_default (bool): If true, all resources will be added to this project if no project is specified.
        created_at (datetime): The time when the project was created.
        updated_at (datetime): The time when the project was updated.
    """
    _url = "projects"
    """
    The url for the projects endpoint
    """
    _plural = "projects"
    """
    The dictionary index used when fetching multiple projects
    """
    _single = "project"
    """
    The dictionary index used when fetching single project.
    """
    _fetch_attrs = ["id"]
    """
    A list of attributes that can be used to fetch a single project.
    """
    _dynamic_attrs = ["name", "description", "purpose", "environment", "is_default"]
    """
    The attribute that can be changed on projects.
    """
    _static_attrs = ["owner_uuid", "owner_id", "created_at", "updated_at"]
    """
    Project attributes that cannot be changed.
    """
    _action_attrs = []
    """
    List of project defined actions.
    """
    _delete_attr = "id"
    """
    The attribute used when deleting a project.
    """
    _update_attr = "id"
    """
    The attribute used when updating a project.
    """
    _action_attr = ""
    """
    The attribute used when calling actions.
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "project"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(Project)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Project id: {self.id}>"
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of project instances.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)

        Return:
            list : A list of project instances.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        projects = super().list(**kwargs)
        ret = []
        for project in projects:
            ret.append(cls(project))
        return ret
    @classmethod
    def getDefault(cls):
        """
        Return the default project objects

        Return:
            Project : The Project for the default project
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls(cls().get(f"{cls.url}/default")[cls.single])

class Purpose:
    """
    A class that contains valid values for the project's purpose attribute.
    """
    trying = "Just trying out DigitalOcean"
    """
    A project to try Digital Ocean services.
    """
    education = "Class project / Educational purposes"
    """
    A project for educational purposes.
    """
    blog = "Website or blog"
    """
    A project for a blog or website.
    """
    web = "Web Application"
    """
    A project to host a web application.
    """
    api = "Service or API"
    """
    A project to host an API.
    """
    mobile = "Mobile Application"
    """
    A project for a mobile application.
    """
    ai = "Machine learning / AI / Data processing"
    """
    A project for Artificial Intelligence purposes.
    """
    iot = "IoT"
    """
    A project for an IOT platform.
    """
    tools = "Operational / Developer tooling"
    """
    A project for Developer and Operational tools
    """
