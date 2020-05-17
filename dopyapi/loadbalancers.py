from .resource import Resource
from .regions import Region
from .droplets import Droplet

class LoadBalancer(Resource):
    """
    This class is used to manage Load Balancer in Digital Ocean.

    You can use this class to create, update and delete load balancers
    and assign droplets to them, also specify their forwarding rules.

    Attributes:
        id (str): A unique ID that can be used to identify and reference a load balancer.
        name (str): A human-readable name for a load balancer instance.
        ip (str): An attribute containing the public-facing IP address of the load balancer.
        alogrithm (str): The load balancing algorithm used to determine which backend Droplet
            will be selected by a client. It must be either "round_robin" or "least_connections".
        status (str): A status string indicating the current state of the load balancer. This can be
            "new", "active", or "errored".
        created_at (datetime.datetime): A time value that represents when the load balancer was created.
        forwarding_rules (list) : A list of objects specifying the forwarding rules for a load balancer.
        health_checks (HealthCheck) : An object specifying health check settings for the load balancer.
        sticky_sessions (StickySession) : An object specifying sticky sessions settings for the load balancer.
        region (Region): The region where the load balancer instance is located.
        tag (str): The name of a Droplet tag corresponding to Droplets assigned to the load balancer.
        droplet_ids (list): A list containing the IDs of the Droplets assigned to the load balancer.
        redirect_http_to_https (bool): A boolean value indicating whether HTTP requests to the load balancer
            on port 80 will be redirected to HTTPS on port 443.
        enable_proxy_protocol (bool): A boolean value indicating whether PROXY Protocol is in use.
    """
    _url = "load_balancers"
    """
    The URL used for the load balancers endpoint
    """
    _plural = "load_balancers"
    """
    The dictionary key used when fetching multiple laod balancers
    """
    _single = "load_balancer"
    """
    The dictionary key used when fetching a single laod balancer
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a load balancer by their value
    """
    _static_attrs = ["ip", "status", "created_at"]
    """
    These attributes are set by Digital Ocean for a load balancer and cannot be changed directly
    """
    _dynamic_attrs = ["name", "region", "algorithm", "forwarding_rules", "health_check", "sticky_sessions", "redirect_http_to_https", "enable_proxy_protocol", "droplet_ids", "tag"]
    """
    These attributes can be used when creating a new load balancer or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the load balancer, each one is a function that return action object
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete load balancers by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update load balancers by its value
    """
    _action_attr = "id"
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "load_balancer"
    """
    This holds the type of resource.
    """

    def __init__(self, data=None):
        super().__init__(LoadBalancer)
        if data is not None:
            self._update({self._single: data})
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of load balancers as defined by its arguments

        Arguments:
            page (int): The page to fetch from all load balancers (defaults 1)
            per_page (int): The number of load balancers per a single page (defaults 20)

        Returns:
            list: A list of load balancers
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        lbs = super().list(**kwargs)
        ret = []
        for lb in lbs:
            ret.append(cls(lb))
        return ret
    def create(self, **kwargs):
        """
        Create a new load balancer

        If no forwarding rule is specified then a default one that forwards
        HTTP traffic on port 80 to port 80 without SSL is used.

        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        forwarding_rules = kwargs.get("forwarding_rules", None)
        if forwarding_rules is None:
            kwargs["forwarding_rules"] = [ForwardingRule()]
        return super().create(**kwargs)
    @property
    def droplets(self):
        ret = []
        for id in self.droplet_ids:
            droplet = Droplet()
            droplet.id = id
            ret.append(droplet)
        return ret
    @property
    def rules(self):
        return self.forwarding_rules
    def addDroplets(self, droplets):
        """
        Add new droplets to the load balancer.

        If the load balancer was created with a tag attribute, then
        this method will throw an error because you cannot add
        droplets to load balancers with a tag attribute, droplets
        in this case are added automatically when you tag a droplet
        with this tag, you can pass a single droplet object, or a list
        of droplet objects, you can also pass IDs instead of objects.

        Args:
            droplets (list): A list of droplets to add, you can pass a
                single droplet and it will be converted to a list.
        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if not isinstance(droplets, list):
            droplets = [droplets]
        droplet_ids = []
        for droplet in droplets:
            if isinstance(droplet, Droplet):
                droplet_ids.append(droplet.id)
            else:
                droplet_ids.append(droplet)
        return self.post(url=f"{self._url}/{self.id}/droplets", data = {"droplet_ids": droplet_ids})
    def deleteDroplets(self, droplets):
        """
        Delete droplets from a load balancer.

        Args:
            droplets (list): A list of droplets to delete, you can pass a
                single droplet and it will be converted to a list.
        Returns:
            dict: A dictionary with one key "status" and value "deleted".
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if not isinstance(droplets, list):
            droplets = [droplets]
        droplet_ids = []
        for droplet in droplets:
            if isinstance(droplet, Droplet):
                droplet_ids.append(droplet.id)
            else:
                droplet_ids.append(droplet)
        return self.delete(url=f"{self._url}/{self.id}/droplets", data = {"droplet_ids": droplet_ids})
    def addRules(self, rules):
        """
        Add new rules to the load balancer.

        Use this method to update the forwarding rules of a load
        balancer.

        Args:
            rules (list): A list of rules to add, you can pass a
                single :class:`~dopyapi.loadbalancers.ForwardingRule` object and it will be converted to a list.
        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if not isinstance(rules, list):
            rules = [rules]
        return self.post(url=f"{self._url}/{self.id}/forwarding_rules", data = {"forwarding_rules": rules})
    def deleteRules(self, rules):
        """
        Delete rules from a load balancer.

        Args:
            rules (list): A list of rules to delete, you can pass a
                single :class:`~dopyapi.loadbalancers.ForwardingRule` object and it will be converted to a list.
        Returns:
            dict: A dictionary with one key "status" and value "deleted".
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if not isinstance(rules, list):
            rules = [rules]
        return self.delete(url=f"{self._url}/{self.id}/forwarding_rules", data = {"forwarding_rules": rules})
class ForwardingRule(object):
    """
    This class represents a single forwarding rule for Load Balancers

    These rules specify how traffic is routed from load balancer to
    internal droplets assigned for the load balancer, it tells type of
    traffic it accepts, port and how to send traffic to the droplet, it
    also tells whether SSL traffic is terminated at the load balancer
    or the droplets assigned to it.

    Attributes:
        entry_protocol (str): The protocol used for traffic to the load balancer.
            The possible values are: "http", "https", "http2", or "tcp". (default http)
        entry_port (int): An integer representing the port on which the load balancer
            instance will listen. (default 80)
        target_protocol (str): The protocol used for traffic from the load balancer to
            the backend Droplets. The possible values are: "http", "https", "http2",
            or "tcp". (default http)
        target_port (int): An integer representing the port on the backend Droplets to
            which the load balancer will send traffic. (default 80)
        certificate_id (str): The ID of the TLS certificate used for SSL termination if enabled.
        tls_passthrough (bool): A boolean value indicating whether SSL encrypted traffic will be
            passed through to the backend Droplets. (default true)

    """

    def __init__(self, entry_protocol="http", entry_port=80,
        target_protocol="http", target_port=80, certificate_id="",
        tls_passthrough=False):
        self.entry_protocol = entry_protocol
        self.entry_port = entry_port
        self.target_protocol = target_protocol
        self.target_port = target_port
        self.certificate_id = certificate_id
        self.tls_passthrough = tls_passthrough

    def __str__(self):
        ret = {
            "entry_protocol": self.entry_protocol,
            "entry_port": self.entry_port,
            "target_protocol": self.target_protocol,
            "target_port": self.target_port,
            "certificate_id": self.certificate_id,
            "tls_passthrough": self.tls_passthrough
        }
        return str(ret)
    def getJSON(self):
        """
        Return the JSON representation of a forwarding rule.

        This will be used when sending API requests to create a load balancer.

        Return:
            dict : A dictionary of key/value pairs for the rule's attributes.
        """
        ret = {
            "entry_protocol": self.entry_protocol,
            "entry_port": self.entry_port,
            "target_protocol": self.target_protocol,
            "target_port": self.target_port,
            "certificate_id": self.certificate_id,
            "tls_passthrough": self.tls_passthrough
        }
        return ret

class HealthCheck(object):
    """
    This class represents health check objects for Digital Ocean Load Balancer

    The health check is used to tell if a droplet is responding or not. The
    load balancer automatically stops sending traffic to unhealthy droplets.

    Attributes:
        protocol (str): The protocol used for health checks sent to the backend
            Droplets. The possible values are "http" or "tcp".
        port (int): An integer representing the port on the backend Droplets
            on which the health check will attempt a connection.
        path (str): The path on the backend Droplets to which the load balancer
            instance will send a request.
        check_interval_seconds (int): The number of seconds between between two consecutive health checks.
        response_timeout_seconds (int): The number of seconds the load balancer instance will wait for a
            response until marking a health check as failed.
        unhealthy_threshold (int): The number of times a health check must fail for a backend Droplet to
            be marked "unhealthy" and be removed from the pool.
        healthy_threshold (int): The number of times a health check must pass for a backend Droplet to be
            marked "healthy" and be re-added to the pool.
    """
    def __init__(self, protocol="http", port=80, path="/", check_interval_seconds=10, response_timeout_seconds=5, healthy_threshold=5, unhealthy_threshold=3):
        self.protocol = protocol
        self.port = port
        self.path = path
        self.check_interval_seconds = check_interval_seconds
        self.response_timeout_seconds = response_timeout_seconds
        self.healthy_threshold = healthy_threshold
        self.unhealthy_threshold = unhealthy_threshold
    def __str__(self):
        return str({
            "protocol": self.protocol,
            "port": self.port,
            "path": self.path,
            "check_interval_seconds": self.check_interval_seconds,
            "response_timeout_seconds": self.response_timeout_seconds,
            "healthy_threshold": self.healthy_threshold,
            "unhealthy_threshold": self.unhealthy_threshold
        })
    def getJSON(self):
        return {
            "protocol": self.protocol,
            "port": self.port,
            "path": self.path,
            "check_interval_seconds": self.check_interval_seconds,
            "response_timeout_seconds": self.response_timeout_seconds,
            "healthy_threshold": self.healthy_threshold,
            "unhealthy_threshold": self.unhealthy_threshold
        }

class StickySession(object):
    """
    A class to represent sticky sessions used in Digital Ocean Load Balancer

    Attributes:
        type (str): An attribute indicating how and if requests from a client will
            be persistently served by the same backend Droplet. The possible values
            are "cookies" or "none". If not specified, the default value is "none".
        cookie_name (str): The name to be used for the cookie sent to the client.
            This attribute is required when using "cookies" for the sticky sessions type.
        cookie_ttl_seconds (int): The number of seconds until the cookie set by the load balancer expires.
            This attribute is required when using "cookies" for the sticky sessions type.
    """
    def __init__(self, type="none", cookie_name = "do-lb", cookie_ttl_seconds=60):
        self.type = type
        self.cookie_name = cookie_name
        self.cookie_ttl_seconds = cookie_ttl_seconds
    def getJSON(self):
        if self.type == "none":
            return {
                "type": "none"
            }
        return {
            "type": self.type,
            "cookie_name": self.cookie_name,
            "cookie_ttl_seconds": self.cookie_ttl_seconds
        }
    def __str__(self):
        if self.type == "none":
            return str({
                "type": "none"
            })
        return str({
            "type": self.type,
            "cookie_name": self.cookie_name,
            "cookie_ttl_seconds": self.cookie_ttl_seconds
        })
