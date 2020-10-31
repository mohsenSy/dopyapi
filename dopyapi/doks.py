"""A module used to interact with Digital Ocean Kuberenetes Cluster API."""
import time
from .resource import Resource

DOKS_V_17 = "1.17.13"
"""Kuberenetes Version 17 slug"""
DOKS_V_18 = "1.18.10"
"""Kuberenetes Version 18 slug"""
DOKS_V_19 = "1.19.3"
"""Kuberenetes Version 19 slug"""


class Node:
    """
    This class represents a single node in the Node Pool.

    Each node has these attributes

    Attributes:
        id (str): A unique ID that can be used to identify and reference the
            node.
        name (str): An automatically generated, human-readable name for the
            node.
        status (dict): An object containing a "state" attribute whose value is
            set to a string indicating the current status of the node.
            Potentialvalues include running, provisioning, and errored.
        created_at (datetime): A time value given in ISO8601 combined date and
            time format that represents when the node was created.
        updated_at (datetime): A time value given in ISO8601 combined date and
            time format that represents when the node was created.
    """

    def __init__(self, id=None, name=None, status=None, created_at=None,
                 updated_at=None, droplet_id=None):
        """Create a new instance of :class:`~dopyapi.doks.Node`."""
        self.id = id
        self.name = name
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.droplet_id = droplet_id

    def __repr__(self):
        """Return a string representation of :class:`~dopyapi.doks.Node`."""
        return f"<Node name: {self.name}, status: {self.status['state']}>"


class NodePool:
    """
    This class represents a pool of ndoes for kubernetes clusters.

    Each pool of nodes defines a number of nodes with a specific size
        name, labels and auto_scale attribute.

    Attributes:
        size (str): The slug identifier for the type of Droplet to be used as
            workers in the node pool.
        name (str): A human-readable name for the node pool.
        count (int): The number of Droplet instances in the node pool.
        labels (dict): An object containing a set of Kubernetes labels.
            The keys are user-defined.
        auto_scale (bool): A boolean value indicating whether auto-scaling is
            enabled for this node pool. This requires DOKS versions at least
            1.13.10-do.3, 1.14.6-do.3, or 1.15.3-do.3.
        min_nodes (int): The minimum number of nodes that this node pool can be
            auto-scaled to. This will fail validation if the additional nodes
            will exceed your account droplet limit.
        max_nodes (int): The maximum number of nodes that this node pool can be
            auto-scaled to. This can be 0, but your cluster must contain at
            least 1 node across all node pools.
    """

    def __init__(self, name, size, count, labels={}, tags=[], auto_scale=False,
                 min_nodes=0, max_nodes=0, nodes=[], id=None, taints=[]):
        """Create a new instance of a node pool."""
        self.name = name
        self.size = size
        self.count = count
        self.labels = labels
        self.tags = tags
        self.auto_scale = auto_scale
        self.min_nodes = min_nodes
        self.max_nodes = max_nodes
        self.nodes = [Node(**x) for x in nodes]
        self.id = id
        self.taints = taints

    def __repr__(self):
        """Return a string representation of :class:`~dopyapi.doks.NodePool`."""
        return f"<NodePool name: {self.name}, count: {self.count}, size: {self.size}>"

    def getJSON(self):
        """Return JSON representation of :class:`~dopyapi.doks.NodePool`."""
        return {
            "id": self.id,
            "name": self.name,
            "count": self.count,
            "size": self.size,
            "labels": self.labels,
            "tags": self.tags,
            "auto_scale": self.auto_scale,
            "min_nodes": self.min_nodes,
            "max_nodes": self.max_nodes,
            "taints": self.taints,
            "nodes": self.nodes
        }


class DOKS(Resource):
    """
    This class represents a single kuberenetes cluster in Digital Ocean.

    The kuberenetes cluster simplifies kuberenetes management, it supports
    these versions of kuberenetes (1.16.14-do.0, 1.17.11-do.0, 1.18.9-do.0).

    Attributes:
        id (str): A unique ID that can be used to identify and reference a Kubernetes cluster.
        name (str): A human-readable name for a Kubernetes cluster.
        endpoint (str): The base URL of the API server on the Kubernetes master node.
        region (str): The slug identifier for the region where the Kubernetes cluster is located.
        version (str): The slug identifier for the version of Kubernetes used for the cluster. If set to a minor version (e.g. "1.14"), the latest version within it will be used (e.g. "1.14.6-do.1"); if set to "latest", the latest published version will be used.
        auto_upgrade (bool): A boolean value indicating whether the cluster will be automatically upgraded to new patch releases during its maintenance window.
        surge_upgrade (bool): A boolean value indicating whether surge upgrade is enabled/disabled for the cluster. Surge upgrade makes cluster upgrades fast and reliable by bringing up new nodes before destroying the outdated nodes.
        ipv4 (str): The public IPv4 address of the Kubernetes master node.
        cluster_subnet (str): The range of IP addresses in the overlay network of the Kubernetes cluster in CIDR notation.
        service_subnet (str): The range of assignable IP addresses for services running in the Kubernetes cluster in CIDR notation.
        vpc_uuid (str): A string specifying the UUID of the VPC to which the Kubernetes cluster is assigned.
        tags (list): An array of tags applied to the Kubernetes cluster. All clusters are automatically tagged "k8s" and "k8s:$K8S_CLUSTER_ID."
        maintenance_policy (str): An object specifying the maintenance window policy for the Kubernetes cluster (see table below).
        node_pools (list): An object specifying the details of the worker nodes available to the Kubernetes cluster (see table below).
        created_at (datetime): A time value given in ISO8601 combined date and time format that represents when the Kubernetes cluster was created.
        updated_at (datetime): A time value given in ISO8601 combined date and time format that represents when the Kubernetes cluster was last updated.
        status (str): An object containing a "state" attribute whose value is set to a string indicating the current status of the node. Potential values include running, provisioning, and errored.

    Maintenance Policy

        This is a dictionary which defines when cluster maintenance will run,
        it has the following keys:

            start_time (str): The start time in UTC of the maintenance window policy in 24-hour clock format / HH:MM notation (e.g., 15:00).

            day (str): The day of the maintenance window policy. May be one of "monday" through "sunday", or "any" to indicate an arbitrary week day.

    Node Pools

        This is a list of :class:`~dopyapi.doks.NodePool`.

    """
    _url = "kubernetes/clusters"
    """
    The URL used for the kuberenetes endpoint
    """
    _plural = "kubernetes_clusters"
    """
    The dictionary key used when fetching multiple clusters
    """
    _single = "kubernetes_cluster"
    """
    The dictionary key used when fetching a single cluster
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a cluster by their value
    """
    _static_attrs = ["endpoint", "ipv4", "cluster_subnet",
                     "service_subnet", "created_at", "updated_at", "status"]
    """
    These attributes are set by Digital Ocean for a kubernetes cluster and cannot be changed directly
    """
    _dynamic_attrs = ["name", "region", "auto_upgrade", "surge_upgrade",
                      "tags", "maintenance_policy", "node_pools", "vpc_uuid"]
    """
    These attributes can be used when creating a new cluster or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the kubernetes cluster
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete kubernetes by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update clusters by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "kubernetes_cluster"
    """
    This holds the type of resource.
    """

    def __init__(self, data=None):
        super().__init__(DOKS)
        if data is not None:
            self._update({self._single: data})

    def __repr__(self):
        return f"<Cluster name: {self.name}>"

    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of kubernetes clusters as defined by its arguments.

        Arguments:
            page (int): The page to fetch from all clusters (defaults 1)
            per_page (int): The number of clusters per a single page (defaults 20)

        Returns:
            list: A list of kubernetes clusters
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        clusters = super().list(**kwargs)
        return [cls(x) for x in clusters]

    def waitReady(self):
        """Wait untill the cluster is online, this method returns when it is online."""
        while True:
            if self.status["state"] == "running":
                break
            self.load()
            time.sleep(self.ttl)

    def upgrades(self):
        """
        Return an array of available version upgrades for current cluster.

        Return:
            list : A list of dictionaries for available upgardes, each one
            has these keys:

            slug (str): The verion slug used in Digital Ocean.

            kubernetes_version (str): The corresponding Digital Ocean service.
        """
        url = f"{self._url}/{self.id}/upgrades"
        return self.get(url=url)["available_upgrade_versions"]

    def upgrade(self, version):
        """
        Upgrade current kuberenetes cluster to specific version.

        Attributes:
            verion (str): The slug identifier for the version of Kubernetes to
                upgrade to. Use :meth:`~dopyapi.doks.DOKS.upgrades` method
                for available versions.

        raises:
            :class:`~dopyapi.resource.ResourceNotFoundError`: When the version
                is not available for upgrade
        """
        url = f"{self._url}/{self.id}/upgrade"
        return self.post(url=url, data={"version": version})

    def kubeconfig(self, expiry_seconds=0):
        """
        Get the kubeconfig of the cluster.

        Args:
            expiry_seconds (int): The expiry of the kubeconfig
                in seconds, if not set or 0 is used then a default
                of 7 days is used.
        Returns:
            bytes: A byte object which contains the kubeconfig used
            to connect to the cluster.
        """
        url = f"{self._url}/{self.id}/kubeconfig"
        return self.get(url=url, expiry_seconds=expiry_seconds)

    def credentials(self, expiry_seconds=0):
        """
        Return the credentials of the cluster.

        Args:
            expiry_seconds (int): The expiry of the credentials
                in seconds, if not set or 0 is used then a default
                of 7 days is used.
        Returns:
            dict: A dictionary object which holds keys and values
            used to connect to the cluster, it has these keys
            (server, certificate_authority_data, client_certificate_data
            , client_key_data, token, expires_at).
        """
        url = f"{self._url}/{self.id}/credentials"
        if expiry_seconds != 0:
            return self.get(url=url, expiry_seconds=expiry_seconds)
        return self.get(url=url)

    def listNodePools(self):
        """
        Return a list of node pools in the cluster.

        Return:
            list : A list of :class:`~dopyapi.doks.NodePool` objects.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or when the database cluster engine is redis
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = f"{self._url}/{self.id}/node_pools"
        node_pools = self.get(url=url)["node_pools"]
        return [NodePool(**node_pool) for node_pool in node_pools]

    def getNodePool(self, id):
        """
        Get a node pool by ID.

        Args:
            id (str): The ID of node pool to get.
        Return:
            :class:`~dopyapi.doks.NodePool`: A ndoe pool object.
        raises:
            :class:`~dopyapi.resource.ResourceNotFoundError`: When the
                id of node pool is not found.
        """
        url = f"{self._url}/{self.id}/node_pools/{id}"
        return NodePool(**self.get(url=url)["node_pool"])

    def addNodePool(self, size, name, count, tags=[], labels={},
                    auto_scale=False, min_nodes=0, max_nodes=0, taints=[]):
        """
        Create a new node pool.

        Args:
            size (str): The size of Node Pool.
            name (str): The name of the Node Pool.
            count (int): The number of nodes in the Pool.
            tags (list): An array of tags to be assigned to the pool.
            labels (dictionary): A dictionary of user defined values assigned
                to the pool.
            auto_scale (bool): A boolean value indicating whether auto-scaling
                is enabled for this node pool. This requires DOKS versions at least 1.13.10-do.3, 1.14.6-do.3, or 1.15.3-do.3.
            min_nodes (int): The minimum number of nodes that this node pool can be auto-scaled to. This will fail validation if the additional nodes will exceed your account droplet limit.
            max_nodes (int): The maximum number of nodes that this node pool can be auto-scaled to. This can be 0, but your cluster must contain at least 1 node across all node pools.
            taints (list): An array of taints to apply to all nodes in a pool. Taints will automatically be applied to all existing nodes and any subsequent nodes added to the pool. When a taint is removed, it is removed from all nodes in the pool.
        Returns:
            dict: A dictionary object for the newly created node pool.
        """
        url = f"{self._url}/{self.id}/node_pools"
        data = {
            "size": size,
            "name": name,
            "count": count,
            "tags": tags,
            "labels": labels,
            "auto_scale": auto_scale,
            "min_nodes": min_nodes,
            "max_nodes": max_nodes,
            "taints": taints
        }
        return self.post(url=url, data=data)["node_pool"]

    def updateNodePool(self, id, name, count, tags=[], labels={},
                       auto_scale=False, min_nodes=0, max_nodes=0, taints=[]):
        """
        Update an existing node pool by ID.

        Args:
            id (str): The ID of node pool to update.
            name (str): The name of the Node Pool.
            count (int): The number of nodes in the Pool.
            tags (list): An array of tags to be assigned to the pool.
            labels (dictionary): A dictionary of user defined values assigned
                to the pool.
            auto_scale (bool): A boolean value indicating whether auto-scaling
                is enabled for this node pool. This requires DOKS versions at least 1.13.10-do.3, 1.14.6-do.3, or 1.15.3-do.3.
            min_nodes (int): The minimum number of nodes that this node pool can be auto-scaled to. This will fail validation if the additional nodes will exceed your account droplet limit.
            max_nodes (int): The maximum number of nodes that this node pool can be auto-scaled to. This can be 0, but your cluster must contain at least 1 node across all node pools.
            taints (list): An array of taints to apply to all nodes in a pool. Taints will automatically be applied to all existing nodes and any subsequent nodes added to the pool. When a taint is removed, it is removed from all nodes in the pool.
        Returns:
            dict: A dictionary object with one key status.
        raises:
            :class:`~dopyapi.resource.ResourceNotFoundError`: When the node pool is not found.
        """
        url = f"{self._url}/{self.id}/node_pools/{id}"
        data = {
            "name": name,
            "count": count,
            "tags": tags,
            "labels": labels,
            "auto_scale": auto_scale,
            "min_nodes": min_nodes,
            "max_nodes": max_nodes,
            "taints": taints
        }
        return self.put(url=url, data=data)

    def deleteNodePool(self, id):
        """
        Delete an existing node pool by ID.

        Args:
            id (str): The ID of node pool to delete.
        Returns:
            dict: A dictionary object of one key status.
        """
        url = f"{self._url}/{self.id}/node_pools/{id}"
        return self.delete(url=url)

    def listNodes(self, id):
        """
        Return a list of nodes in a pool by ID.

        Args:
        id (str): The ID of node pool to get its nodes.

        Return:
            list : A list of :class:`~dopyapi.doks.Node` objects.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or when the database cluster engine is redis
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = f"{self._url}/{self.id}/node_pools/{id}"
        return self.get(url=url)["node_pool"]["nodes"]

    def deleteNode(self, id, node_id, replace=0, skip_drain=0):
        """
        Delete an existing node in a node pool by its ID.

        Args:
            id (str): The ID of node pool.
            node_id (str): The ID of node to delete.
        Returns:
            dict: A dictionary object with one key status.
        """
        url = f"{self._url}/{self.id}/node_pools/{id}/nodes/{node_id}"
        return self.delete(url=url, replace=replace, skip_drain=skip_drain)

    def clusterlintCheck(self):
        """Run a clusterlint on the kuberenetes cluster."""
        url = f"{self._url}/{self.id}/clusterlint"
        return self.post(url=url, data={})

    def clusterlint(self, run_id=None):
        """
        Retrieve clusterlint diagnostic.

        If no run_id is provided then the last one is used.

        Args:
            run_id (str): The clusterlint run id to fetch.
        """
        url = f"{self._url}/{self.id}/clusterlint"
        return self.get(url=url, run_id=run_id)

    def options(self):
        """Return an object of available versions and sizes."""
        url = "kubernetes/options"
        return self.get(url)
