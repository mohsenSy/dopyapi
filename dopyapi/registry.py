import os
import json
from .resource import Resource, ResourceNotFoundError, ClientError

class DockerCredentials:
    """
    This class is used to store docker credentials for a docker registry
    in Digital Ocean.
    """
    def __init__(self, cred):
        self.__cred = cred
    def apply(self, file_name=f"{os.environ['HOME']}/.docker/config.json"):
        """
        Use this function to save the docker credentials to your docker
        configuration file

        Args:
            file_name (str): The name of the file that contains docker credentials
                default value is ``$HOME/.docker/config.json``
        """
        with open(file_name, "r+") as file:
            current_config = json.loads(file.read())
        registry_domain = str(list(self.__cred["auths"].keys())[0])
        current_config["auths"][registry_domain] = self.__cred["auths"][registry_domain]
        with open(file_name, "w") as file:
            file.write(json.dumps(current_config, sort_keys=True, indent=4))
    def __str__(self):
        return json.dumps(str(self.__cred), sort_keys=True, indent=4)

class RepositoryTag(Resource):
    """
    This class represents a single tgged repository image in your registry.

    Attributes:
        registry_name (str): The name of the container registry.
        repository (str): The name of the repository.
        tag (str) : The name of the tag.
        manifest_digest (str): The digest of the manifest associated with the tag.
        compressed_size_bytes (int): The compressed size of the tag in bytes.
        size_bytes (int): The uncompressed size of the tag in bytes (this size is calculated asynchronously so it may not be immediately available).
        updated_at (datetime): The time the tag was last updated.
    """
    _url = "registry/{}/repositories/{}/tags"
    """
    The url used for the repository tag endpoint
    """
    _plural = "tags"
    """
    The dictionary index used when fetching multiple repository tag.
    """
    _single = "tag"
    """
    The dictionary index used when fetching single repository tag
    """
    _fetch_attrs = []
    """
    A list of attributes that can be used to fetch repository tags based on them.
    """
    _dynamic_attrs = [""]
    """
    A list of attributes that can be used when creating or updating a new repository tags
    """
    _static_attrs = ["registry_name", "repository", "tag", "manifest_digest", "compressed_size_bytes", "size_bytes", "updated_at"]
    """
    A list of attributes that are set by Digital Ocean and cannot be changed directly.
    """
    _action_attrs = []
    """
    A list of actions for repository tags.
    """
    _delete_attr = "tag"
    """
    The attribute used when deleting a repository tag.
    """
    _update_attr = ""
    """
    The attribute used when updating a repository tag.
    """
    _action_attr = ""
    """
    The attribute used when calling actions, no actions here.
    """
    _resource_type = "repository_tag"
    """
    The type of resource, it is used when tagging resources.
    """
    _id_attr = "tag"
    """
    The attribute used as a unique identifier for the repository
    """
    def __init__(self, registry_name, repository_name, data=None):
        super().__init__(RepositoryTag)
        self._url = self._url.format(registry_name, repository_name)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<RepositoryTag tag: {self.tag}>"
    def __str__(self):
        return str(self.tag)
    def deleteByDigest(self):
        """
        Delete current repository tag using its manifest digest value.
        """
        url = f"{self._url}/digests/{self.manifest_digest}"
        return super().delete(url=url)

class Registry(Resource):
    """
    This class represents the container registry in your account.

    Attributes:
        name (str): The name of the container registry to validate.
    """
    _url = "registry"
    """
    The url used for the registry endpoint
    """
    _plural = "registry"
    """
    The dictionary index used when fetching multiple registries.
    """
    _single = "registry"
    """
    The dictionary index used when fetching single registry
    """
    _fetch_attrs = []
    """
    A list of attributes that can be used to fetch registries based on them.
    """
    _dynamic_attrs = ["name"]
    """
    A list of attributes that can be used when creating or updating a new registry
    """
    _static_attrs = ["created_at"]
    """
    A list of attributes that are set by Digital Ocean and cannot be changed directly.
    """
    _action_attrs = []
    """
    A list of actions for registries.
    """
    _delete_attr = ""
    """
    The attribute used when deleting a registry
    """
    _update_attr = ""
    """
    The attribute used when updating a registry.
    """
    _action_attr = ""
    """
    The attribute used when calling actions, no actions here.
    """
    _resource_type = "registry"
    """
    The type of resource, it is used when tagging resources.
    """
    _id_attr = "name"
    """
    The attribute used as a unique identifier for the registry
    """
    def __init__(self, data=None):
        super().__init__(Registry)
        try:
            d = self.get(self._url)
            self._update(d)
        except ResourceNotFoundError:
            pass
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Registry name: {self.name}>"
    def __str__(self):
        return str(self.name)
    def delete(self):
        return super().delete(url=self._url)
    def getDockerCredentials(self, read_write=False, expiry_seconds=None):
        """
        Get the docker credentials for this registry.

        Returns:
            DockerCredentials: An object that contains the docker credentials.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return DockerCredentials(self.get(url=f"{self._url}/docker-credentials", read_write=read_write, expiry_seconds=expiry_seconds))
    def validate(self, name):
        """
        Make sure the passed name is a valid name for docker registry
        and can be used here.

        Args:
            name (str): The name to validate.
        Returns:
            bool: True if name is valid and False otherwise
        """
        try:
            self.post(f"{self._url}/validate-name", {"name": name})
            return True
        except ClientError:
            return False

class Repository(Resource):
    """
    This class represents the container Repository in your registry.

    Attributes:
        registry_name (str): The name of the container registry.
        name (str): The name of the repository.
        latest_tag (RepositoryTag) : The latest tag of the repository.
        tag_count (int): The number of tags in the repository.
    """
    _url = "registry/{}/repositories"
    """
    The url used for the repository endpoint
    """
    _plural = "repositories"
    """
    The dictionary index used when fetching multiple repositories.
    """
    _single = "repository"
    """
    The dictionary index used when fetching single repository
    """
    _fetch_attrs = []
    """
    A list of attributes that can be used to fetch repositories based on them.
    """
    _dynamic_attrs = ["name"]
    """
    A list of attributes that can be used when creating or updating a new repositories
    """
    _static_attrs = ["registry_name", "tag_count", "latest_tag", "name"]
    """
    A list of attributes that are set by Digital Ocean and cannot be changed directly.
    """
    _action_attrs = []
    """
    A list of actions for repositories.
    """
    _delete_attr = ""
    """
    The attribute used when deleting a repository.
    """
    _update_attr = ""
    """
    The attribute used when updating a repository.
    """
    _action_attr = ""
    """
    The attribute used when calling actions, no actions here.
    """
    _resource_type = "repository"
    """
    The type of resource, it is used when tagging resources.
    """
    _id_attr = "name"
    """
    The attribute used as a unique identifier for the repository
    """
    def __init__(self, registry_name, data=None):
        super().__init__(Repository)
        self._url = self._url.format(registry_name)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Repository name: {self.name}>"
    def __str__(self):
        return str(self.name)
    @classmethod
    def list(cls, registry_name, **kwargs):
        """
        Return a list of repositories based on arguments

        Arguments:
            registry_name (str): The name of the Container Registry
            page (int): The page to fetch (defaults 1)
            per_page (int): The number of repositories in the page (defaults 20)
        Return:
            list: A list of repository objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        reps = super().list(url=cls._url.format(registry_name), **kwargs)
        return [cls(registry_name, rep) for rep in reps]
    def listTags(self, **kwargs):
        """
        Return a list of repositoriy tags based on arguments

        Arguments:
            page (int): The page to fetch (defaults 1)
            per_page (int): The number of repository tags in the page (defaults 20)
        Return:
            list: A list of repository tag objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = "{}/{}/tags".format(self._url.format(self.registry_name), self.name)
        tags = super().list(url=url, index="tags", **kwargs)
        return [RepositoryTag(self.registry_name, self.name, tag) for tag in tags]
