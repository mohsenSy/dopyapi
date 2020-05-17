from .resource import Resource
from .droplets import Droplet
from .tags import Tag

class Firewall(Resource):
    """
    This class represents firewalls in DigitalOcean

    You can use this class to create, update, delete and manage firewalls
    on your Digital Ocean account, all firewall attributes are available too.

    Attributes:
        id (str): A unique identifier for the firewall, it is generated
            when the firewall is created.
        name (str): A human readable name for the firewall
        pending_changes (list): A list of dictionaries each containing the fields
            "droplet_id", "removing", and "status". It is provided to detail exactly
            which Droplets are having their security policies updated. When empty,
            all changes have been successfully applied.
        created_at (datetime.datetime): A time object that tells when the firewall
            was created.
        status (str): A status string indicating the state of the firewall, it could
            be ("waiting", "succeeded", "failed").
        inbound_rules (list): A list of :class:`InboundRule` objects which specify inbound rules applied
            in the firewall.
        outbound_rules (list): A list of :class:`OutboundRule` which specify outbound rules applied
            in the firewall.
        droplet_ids (list): A list containing the IDs of the Droplets assigned to the firewall.
        tags (list): A list containing the names of the Tags assigned to the firewall.
    """
    _url = "firewalls"
    """
    The URL used for the firewalls endpoint
    """
    _single = "firewall"
    """
    The dictionary key used when fetching a single firewall
    """
    _plural = "firewalls"
    """
    The dictionary key used when fetching multiple firewalls
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a firewall by their value
    """
    _dynamic_attrs = ["inbound_rules", "outbound_rules", "name", "droplet_ids", "tags"]
    """
    These attributes can be used when creating a new firewall or updating an existing one
    """
    _static_attrs = ["status", "created_at", "pending_changes"]
    """
    These attributes are set by Digital Ocean for a firewall and cannot be changed directly
    """
    _action_attrs = []
    """
    These are the actions that can be used with the firewall, each one is a function that return action object
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete firewalls by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update firewalls by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "firewall"
    """
    This holds the type of resource.
    """
    def __init__(self, data=None):
        super().__init__(Firewall)
        if data is not None:
            self._update({self._single: data})
    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of firewalls as defined by its arguments

        Arguments:
            page (int): The page to fetch from all firewalls (defaults 1)
            per_page (int): The number of firewalls per a single page (defaults 20)

        Returns:
            list: A list of firewalls
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        fws = super().list(**kwargs)
        ret = []
        if fws is None:
            return ret
        for fw in fws:
            ret.append(cls(fw))
        return ret
    def __str__(self):
        return f"<Firewall id: {self.id}, status: {self.status}>"
    def __repr__(self):
        return f"<Firewall id: {self.id}, status: {self.status}>"
    def create(self, name, inbound_rules = [], outbound_rules=[]):
        """
        Create a new Firewall

        This method is used to create a new Firewall, if no rules are specified
        then these defaults are used:
        * An outbound rule that allows ICMP to all destinations.
        * An outbound rule that allows TCP to all ports and destinations.
        * An outbound rule that allows UDP to all ports and destinations.

        Args:
            name (str): The name of the firewall
            inbound_rules (list): A list of `InboundRule` objects. default []
            outbound_rules (list): A list of `OutboundRule` objects. default []
        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if outbound_rules == [] and inbound_rules == []:
            destinations = Location(addresses = ["0.0.0.0/0", "::/0"])
            outbound_rule1 = OutboundRule(protocol="icmp", destinations=destinations)
            outbound_rule2 = OutboundRule(protocol="udp", ports="all", destinations=destinations)
            outbound_rule3 = OutboundRule(protocol="tcp", ports="all", destinations=destinations)
            outbound_rules = [outbound_rule1, outbound_rule2, outbound_rule3]
        return super().create(name=name, inbound_rules=inbound_rules, outbound_rules=outbound_rules)
    def addDroplets(self, ids):
        """
        Add droplets to this Firewall

        When adding droplets to a firewall, its rules are applied
        to traffic that tries to enter the droplet.

        Args:
            ids (list): A list of droplets to be added, if you use a single
                value it will be converted to a list for you.
        Returns:
            dictionary: JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if not isinstance(ids, list):
            ids = [ids]
        data = {
            "droplet_ids": ids
        }
        return self.post(f"{self._url}/{self.getID()}/droplets", data = data)
    def removeDroplets(self, ids):
        """
        Remove droplets from the Firewall

        Args:
            ids (list, Droplet): A list of IDs or droplet objects to remove,
                you can pass a single ID or droplet here.
        Returns:
            dictionary: JSON object from the API
        Raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if not isinstance(ids, list):
            ids = [ids]
        data = {
            "droplet_ids": ids
        }
        return self.delete(url=f"{self._url}/{self.getID()}/droplets", data = data)
    def addTags(self, tags):
        """
        Add tags to the firewall

        Args:
            tags (list, Tag): A list of tags to add, it could be tag names
                or tag objects, if you use a single name or object it is
                converted to a list for you.
        Returns:
            list: The JSON response from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if not isinstance(tags, list):
            tags = [tags]
        data = {
            "tags": tags
        }
        return self.post(f"{self._url}/{self.getID()}/tags", data = data)
    def removeTags(self, tags):
        """
        Remove tags from the Firewall

        Args:
            ids (list, Tag): A list of IDs or tag objects to remove,
                you can pass a single ID or tag here.
        Returns:
            dictionary: JSON object from the API
        Raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if not isinstance(tags, list):
            tags = [tags]
        data = {
            "tags": tags
        }
        return self.delete(url=f"{self._url}/{self.getID()}/tags", data = data)
    def addRules(self, rules):
        """
        Add rules to the firewall

        Args:
            tags (list, InboundRule, OutboundRule): A list of rules to add,
                if you use a single object it is converted to a list for you.
        Returns:
            list: The JSON response from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if not isinstance(rules, list):
            rules = [rules]
        inbound_rules = [rule for rule in rules if isinstance(rule, InboundRule)]
        outbound_rules = [rule for rule in rules if isinstance(rule, OutboundRule)]
        data = {
            "inbound_rules": inbound_rules,
            "outbound_rules": outbound_rules
        }
        return self.post(f"{self._url}/{self.getID()}/rules", data = data)
    def removeRules(self, tags):
        """
        Remove rules from the Firewall

        Args:
            ids (list, InboundRule, OutboundRule): A list of IDs or rule objects to remove,
                you can pass a single ID or rule object here.
        Returns:
            dictionary: JSON object from the API
        Raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if not isinstance(rules, list):
            rules = [rules]
        inbound_rules = [rule for rule in rules if isinstance(rule, InboundRule)]
        outbound_rules = [rule for rule in rules if isinstance(rule, OutboundRule)]
        data = {
            "inbound_rules": inbound_rules,
            "outbound_rules": outbound_rules
        }
        return self.delete(url=f"{self._url}/{self.getID()}/rules", data = data)
    @property
    def droplets(self):
        """
        Return droplet objects which are added to this firewall

        Returns:
            list: A list of droplet objects
        """
        ret = []
        for id in self.droplet_ids:
            droplet = Droplet()
            droplet.id = id
            ret.append(droplet)
        return ret



class Location(object):
    """
    This class represents sources or destinations for firewall inbound and outbound rules.

    A location could be a droplet, load balancer, Individual IP address or ranges
        of them and droplets by tag.

    Attributes:
        addresses (list): A list of strings containing the IPv4 addresses, IPv6 addresses,
            IPv4 CIDRs, and/or IPv6 CIDRs to which the firewall will allow traffic.
        droplet_ids (list): A list containing the IDs of the Droplets to which the firewall will allow traffic.
        load_balancer_uids (list): A list containing the IDs of the load balancers to which the firewall will allow traffic.
        tags (list): A list containing the names of Tags corresponding to groups of Droplets to which the firewall will allow traffic.
    """
    def __init__(self, addresses=[], droplet_ids=[], load_balancer_uids=[], tags=[]):
        self.addresses = addresses
        self.droplet_ids = droplet_ids
        self.load_balancer_uids = load_balancer_uids
        self.tags = tags

    def getJSON(self):
        """
        Return a JSON representation of a location object

        This representation is used when making API calls.

        Returns:
            dict : A dictionary for the location object
        """
        return {
            "addresses": self.addresses,
            "droplet_ids": self.droplet_ids,
            "load_balancer_uids": self.load_balancer_uids,
            "tags": self.tags
        }

    def __str__(self):
        return f"<Location addresses: {self.addresses}>"
    def __repr__(self):
        return f"<Location addresses: {self.addresses}>"

class Rule(object):
    """
    This class is the base class for inbound and outbound rules in Digital Ocean firewalls.

    Here we find the protocol and ports attributes for a rule, the rest of attributes
        can be found in :class:`InboundRule` and :class:`OutboundRule` classes.

    Attributes:
        protocol (str): The type of traffic to be allowed. This may be one of "tcp", "udp", or "icmp".
        ports (str): The ports on which traffic will be allowed specified as a string containing
            a single port, a range (e.g. "8000-9000"), or "0" when all ports are open for a protocol.
            For ICMP rules this parameter will always return "0".
    """

    def __init__(self, protocol = "tcp", ports = "all"):
        if protocol not in ["tcp", "udp", "icmp"]:
            raise RuleError(f"protocol can only be one of 'tcp', 'udp' and 'icmp', found {protocol}")
        self.protocol = protocol
        if self.protocol == "icmp":
            self.ports = None
        else:
            self.ports = ports


class InboundRule(Rule):
    """
    This class is used to represent an inbound rule in Digital Ocean Firewall

    An inbound rule is applied when packets enter the firewall, it specifies
    what data is allowed in and any other data that does not match any
    inbound rule for a firewall is discarded and not allowed to reach the
    resources associated with the firewall.

    Attributes:
        sources (Location): An object specifying locations from which inbound traffic will be accepted.
    """

    def __init__(self, protocol = "tcp", ports = "all", sources=None):
        super().__init__(protocol=protocol, ports=ports)
        if sources is None:
            sources = Location()
        if isinstance(sources, dict):
            addresses = sources.get("addresses", None)
            droplet_ids = sources.get("droplet_ids", None)
            load_balancer_uids = sources.get("load_balancer_uids", None)
            tags = sources.get("tags", None)
            self.sources = Location(addresses, droplet_ids, load_balancer_uids, tags)
        else:
            self.sources = sources
    def getJSON(self):
        """
        Return a JSON representation of an inbound rule

        This representation is used when making API calls.

        Returns:
            dict : A dictionary for the inbound rule
        """
        if self.ports is None:
            return {
                "protocol": self.protocol,
                "sources": self.sources.getJSON()
            }
        return {
            "protocol": self.protocol,
            "ports": self.ports,
            "sources": self.sources.getJSON()
        }

    def __str__(self):
        return f"<InboundRule protocol : {self.protocol}, ports: {self.ports}>"
    def __repr__(self):
        return f"<InboundRule protocol : {self.protocol}, ports: {self.ports}>"

class OutboundRule(Rule):
    """
    This class is used to represent an outbound rule in Digital Ocean Firewall

    An outbound rule is applied when packets leave the firewall, it specifies
    what data is allowed out and any other data that does not match any
    outbound rule for a firewall is discarded and not allowed.

    Attributes:
        destinations (Location): An object specifying locations to which outbound traffic will be accepted.
    """

    def __init__(self, protocol = "tcp", ports = "all", destinations=None):
        super().__init__(protocol=protocol, ports=ports)
        if destinations is None:
            destinations = Location()
        if isinstance(destinations, dict):
            addresses = destinations.get("addresses", None)
            droplet_ids = destinations.get("droplet_ids", None)
            load_balancer_uids = destinations.get("load_balancer_uids", None)
            tags = destinations.get("tags", None)
            self.destinations = Location(addresses, droplet_ids, load_balancer_uids, tags)
        else:
            self.destinations = destinations

    def getJSON(self):
        """
        Return a JSON representation of an outbound rule

        This representation is used when making API calls.

        Returns:
            dict : A dictionary for the outbound rule
        """
        if self.ports is None:
            return {
                "protocol": self.protocol,
                "destinations": self.destinations.getJSON()
            }
        return {
            "protocol": self.protocol,
            "ports": self.ports,
            "destinations": self.destinations.getJSON()
        }

    def __str__(self):
        return f"<OutboundRule protocol : {self.protocol}, ports: {self.ports}>"
    def __repr__(self):
        return f"<OutboundRule protocol : {self.protocol}, ports: {self.ports}>"

class RuleError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
