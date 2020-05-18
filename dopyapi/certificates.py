from .resource import Resource, ClientError

class Certificate(Resource):
    """
    This class represents a single certificate in Digital Ocean.

    Certificates can be either, custom (created, uploaded and renewed
    by the user) or managed (Uses let' encrypt free certificates
    and managed by Digital Ocean entrirely).

    Attributes:
        id (str): A unique ID that can be used to identify and reference a certificate.
        name (str): A unique human-readable name referring to a certificate.
        not_after (datetime.datetime): A time value given in ISO8601 combined date and time format that represents the certificate's expiration date.
        sha1_fingerprint (str): A unique identifier generated from the SHA-1 fingerprint of the certificate.
        created_at (datetime.datetime): A time value given in ISO8601 combined date and time format that represents when the certificate was created.
        dns_names (list): An array of fully qualified domain names (FQDNs) for which the certificate was issued.
        state (str): A string representing the current state of the certificate. It may be "pending", "verified", or "error".
        type (str): A string representing the type of the certificate. The value will be "custom" for a user-uploaded certificate or "lets_encrypt" for one automatically generated with Let's Encrypt.
    """
    _url = "certificates"
    """
    The URL used for the certificates endpoint
    """
    _plural = "certificates"
    """
    The dictionary key used when fetching multiple certificates
    """
    _single = "certificate"
    """
    The dictionary key used when fetching a single certificate
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a certificate by their value
    """
    _static_attrs = ["not_after", "created_at", "sha1_fingerprint", "state"]
    """
    These attributes are set by Digital Ocean for a certificate and cannot be changed directly
    """
    _dynamic_attrs = ["name", "type", "dns_names"]
    """
    These attributes can be used when creating a new certificate or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the certificates, each one is a function that return action object
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete a certificate by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update certificates by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "certificate"
    """
    This holds the type of resource.
    """
    def __init__(self, data = None):
        super().__init__(Certificate)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Certificate id:{self.id}, type:{self.type}>"
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of certificates as defined by its arguments

        Arguments:
            page (int): The page to fetch from all certificates (defaults 1)
            per_page (int): The number of certificates per a single page (defaults 20)

        Returns:
            list: A list of certificates
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        endpoints = super().list(**kwargs)
        return [cls(x) for x in endpoints]
    def create(self, name, type = "lets_encrypt", private_key = None, leaf_certificate = None, certificate_chain = None, dns_names = []):
        """
        Create a new SSL certificate

        We need to pass the name of certificate and some other values according
        to its type, if type is 'lets_encrypt' you need to use ``dns_names``
        or if the type is 'custom' you need to use ``private_key``,
        ``leaf_certificate`` and ``certificate_chain``.

        Args:
            name (str): The name of certificate.
            type (str): The type of certificate, it could be either
                'lets_encrypt' or 'custom', default is 'lets_encrypt'
            private_key (str): The private key for certificate, required
                when creating a custom certificate. default is None
            leaf_certificate (str): The contents of a PEM-formatted public SSL certificate.
                required with custom certificates. default is None
            certificate_chain (str): The full PEM-formatted trust chain between the certificate
                authority's certificate and your domain's SSL certificate.
                required with custom certificates. default is None.
            dns_names (list): A list of fully qualified domain names (FQDNs) for which the
                certificate will be issued. The domains must be managed using DigitalOcean's DNS.
                required for lets_encrypt certificates. default is []
        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
                or when reqired attributes use default values, based on certificate
                type.
            ClientForbiddenError : This is raised when the domain is not managed in Digital Ocean.
            ResourceNotFoundError : This is raised when the status code is 404
        """
        cert_data = {
            "name": name,
            "type": type
        }
        if type == "custom":
            if private_key is None and leaf_certificate is None and certificate_chain is None:
                raise ClientError("When creating a custom certificate, you need to use private_key, leaf_certificate and certificate_chain")
            cert_data["private_key"] = private_key
            cert_data["leaf_certificate"] = leaf_certificate
            cert_data["certificate_chain"] = certificate_chain
        elif type == "lets_encrypt":
            if len(dns_names) == 0:
                raise ClientError("When creating a let encrypt certificate, you need to use a list of dns names for the certificate")
            cert_data["dns_names"] = dns_names
        else:
            raise ClientError("Type can only be 'custom' or 'lets_encrypt'")
        return super().create(**cert_data)
