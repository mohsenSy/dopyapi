from .resource import Resource

class SSHKey(Resource):
    """
    This class represents SSHKeys in Digital Ocean.

    SSHKeys are used to embed public keys at droplet creation.

    Attributes:
        id (int): A unique identifier for the key.
        fingerprint (str): The fingerprint value generated from the public key.
        public_key (str): The entire public key as a string.
        name (str): A human readable name for the key.
    """
    _url = "account/keys"
    """
    The API endpoint for SSHKeys.
    """
    _plural = "ssh_keys"
    """
    The dictionary index used when fetching multiple sshkey instances.
    """
    _single = "ssh_key"
    """
    The dictionary index used when fetching single sshkey instance.
    """
    _fetch_attrs = ["id", "fingerprint"]
    """
    The attributes that can be used to fetch sshkey instances.
    """
    _static_attrs = []
    """
    SSHKey attributes that cannot be changed.
    """
    _dynamic_attrs = ["public_key", "name"]
    """
    The attribute that can be changed on snapshots.
    """
    _action_attrs = []
    """
    List of SSHKey defined actions.
    """
    _delete_attr = "id"
    """
    The attribute used when deleting a SSHKey.
    """
    _update_attr = "id"
    """
    The attribute used when updating a SSHKey.
    """
    _action_attr = ""
    """
    The attribute used when calling actions.
    """
    _id_attr = "id"
    """
    The name of attribute used as an ID for SSH Keys.
    """
    _resource_type = "ssh_key"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(SSHKey)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<SSHKey name: {self.name}>"
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of SSHKey instances.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of snapshot instances in a single page. (default 20)

        Return:
            list : A list of SSHKey instances.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        sshkeys = super().list(**kwargs)
        ret = []
        for sshkey in sshkeys:
            ret.append(cls(sshkey))
        return ret
