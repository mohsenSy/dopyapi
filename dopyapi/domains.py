from .resource import Resource, ClientError

class Domain(Resource):
    """
    This class represents a single domain in Digital Ocean.

    Domain records are only managed by Digital Ocean, the domain
    still needs to be bought using a domain registrar, and its NS
    records updated to the ones provided by Digital Ocean.

    Attributes:
        name (str): The name of the domain itself. This should follow the standard domain format of domain.TLD. For instance, example.com is a valid domain name.
        ttl (int): This value is the time to live for the records on this domain, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested.
        zone_file (str): This attribute contains the complete contents of the zone file for the selected domain. Individual domain record resources should be used to get more granular control over records. However, this attribute can also be used to get information about the SOA record, which is created automatically and is not accessible as an individual record resource.
    """
    _url = "domains"
    """
    The URL used for the domains endpoint
    """
    _plural = "domains"
    """
    The dictionary key used when fetching multiple domains
    """
    _single = "domain"
    """
    The dictionary key used when fetching a single domain
    """
    _fetch_attrs = ["name"]
    """
    These attributes can be used to fetch a domain by their value
    """
    _static_attrs = ["zone_file"]
    """
    These attributes are set by Digital Ocean for a domain and cannot be changed directly
    """
    _dynamic_attrs = ["ttl"]
    """
    These attributes can be used when creating a new domain or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the domains, each one is a function that return action object
    """
    _delete_attr = "name"
    """
    This is the name of the attribute used to delete a domain by its value
    """
    _update_attr = "name"
    """
    This is the name of the attribute used to update domains by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "name"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "domain"
    """
    This holds the type of resource.
    """
    def __init__(self, data = None):
        super().__init__(Domain)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<Domain name:{self.name}, ttl:{self.ttl}>"
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of domains as defined by its arguments

        Arguments:
            page (int): The page to fetch from all domains (defaults 1)
            per_page (int): The number of domains per a single page (defaults 20)

        Returns:
            list: A list of domains
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        endpoints = super().list(**kwargs)
        return [cls(x) for x in endpoints]
    def create(self, name, ip_address = None):
        """
        Create a new domain

        We only need to provide the domain's name and optionally
        and IP address to be assigned to the apex record.

        Args:
            name (str): The domain name to add to the DigitalOcean DNS management interface. The name must be unique in DigitalOcean's DNS system. The request will fail if the name has already been taken..
            ip_address (str): This optional attribute may contain an IP address. When provided, an A record will be automatically created pointing to the apex domain. default is None
        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        domain_data = {
            "name": name
        }
        if ip_address is not None:
            domain_data["ip_address"] = ip_address
        return super().create(**domain_data)

from .resource import Resource, ClientError

class DomainRecord(Resource):
    """
    This class represents a single domain record in Digital Ocean.

    Each domain record belongs to a single domain.

    Attributes:
        id (int): A unique identifier for each domain record.
        type (str): The type of the DNS record. For example: A, CNAME, TXT, ...
            You can find a full list bellow.
        name (str): The host name, alias, or service being defined by the record.
        data (str): Variable data depending on record type. For example, the "data" value for an A record would be the IPv4 address to which the domain will be mapped. For a CAA record, it would contain the domain name of the CA being granted permission to issue certificates.
        priority (int): The priority for SRV and MX records.
        port (int): The port for SRV records.
        ttl (int): This value is the time to live for the record, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested.
        weight (int): The weight for SRV records.
        flags (int): An unsigned integer between 0-255 used for CAA records.
        tag (str): The parameter tag for CAA records. Valid values are "issue", "issuewild", or "iodef"

    Record Types:

        A: This record type is used to map an IPv4 address to a hostname.

        AAAA: This record type is used to map an IPv6 address to a hostname.

        CAA: As specified in RFC-6844, this record type can be used to restrict which certificate authorities are permitted to issue certificates for a domain.

        CNAME: This record type defines an alias for your canonical hostname (the one defined by an A or AAAA record).

        MX: This record type is used to define the mail exchanges used for the domain.

        NS: This record type defines the name servers that are used for this zone.

        TXT: This record type is used to associate a string of text with a hostname, primarily used for verification.

        SRV: This record type specifies the location (hostname and port number) of servers for specific services.

        SOA: This record type defines administrative information about the zone. Can only have ttl changed, cannot be deleted
    """
    _url = "domains/{}/records"
    """
    The URL used for the domains records endpoint
    """
    _plural = "domain_records"
    """
    The dictionary key used when fetching multiple domain records
    """
    _single = "domain_record"
    """
    The dictionary key used when fetching a single domain records
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a domain record by their value
    """
    _static_attrs = []
    """
    These attributes are set by Digital Ocean for a domain record and cannot be changed directly
    """
    _dynamic_attrs = ["type", "name", "data", "priority", "port", "ttl", "weight", "flags", "tag"]
    """
    These attributes can be used when creating a new domain record or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the domain records, each one is a function that return action object
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete a domain record by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update domain record by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "domain_record"
    """
    This holds the type of resource.
    """
    _record_types = {
        "A": ["name", "data"],
        "AAAA": ["name", "data"],
        "CAA": ["name", "data", "flags", "tag"],
        "CNAME": ["name", "data"],
        "MX": ["data", "priority"],
        "TXT": ["name", "data"],
        "SRV": ["name", "data", "priority", "port", "weight"],
        "SOA": ["ttl"]
    }
    def __init__(self, domain, data = None):
        """
        Create a new DomainRecord instance, here we need to pass the domain's name

        Args:
            domain (str): The name of the domain to use.
        """
        super().__init__(DomainRecord)
        self.__domain = domain
        self._url = self._url.format(self.__domain)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        return f"<DomainRecord name:{self.name}, type:{self.type}>"
    @classmethod
    def list(cls, domain_name, **kwargs):
        """
        This method returns a list of domain records as defined by its arguments

        Arguments:
            domain_name: The name of the domain to fetch records for it
            page (int): The page to fetch from all domain records (defaults 1)
            per_page (int): The number of domain records per a single page (defaults 20)

        Returns:
            list: A list of domain records
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        domain_records = super().list(url=cls._url.format(domain_name), **kwargs)
        return [cls(domain_name, x) for x in domain_records]
    def create(self, type, **kwargs):
        """
        Create a new domain record

        Here we pass the record's type first, then we pass a number of
        arguments according to the records type.

        Args:
            type (str): The type of the record A, AAAA, MX, etc....
            name (str): The host name, alias, or service being defined by the record. required for A, AAAA, CAA, CNAME, TXT and SRV types.
            data (str): Variable data depending on record type. For example, the "data" value for an A record would be the IPv4 address to which the domain will be mapped. For a CAA record, it would contain the domain name of the CA being granted permission to issue certificates. required for A, AAAA, CAA, CNAME, MX, TXT, SRV, NS
            priority (int): The priority of the host (for SRV and MX records. null otherwise). required for MX and SRV records.
            port (int): The port that the service is accessible on (for SRV records only. null otherwise). reqired for SRV records.
            ttl (int): This value is the time to live for the record, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested. There is a minimum ttl value of 30, unless it is not set. If not set, the default value is the value of the SOA record. For SOA records, defines the time to live for purposes of negative caching. required for SOA records
            weight (int): The weight of records with the same priority (for SRV records only. null otherwise). required for SRV records.
            flags (int): An unsigned integer between 0-255 used for CAA records. required for CAA records.
            tag (str): The parameter tag for CAA records. Valid values are "issue", "issuewild", or "iodef" required for CAA records.
        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : When type is not supported or no enough data to create the record.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if type not in self._record_types.keys():
            raise ClientError(f"{type} record is not supported")
        print(set(self._record_types[type]))
        print(set(kwargs.keys()))
        if not set(self._record_types[type]) <= set(kwargs.keys()):
            raise ClientError(f"For {type} records you need {self._record_types[type]}")
        return super().create(type=type, **kwargs)
