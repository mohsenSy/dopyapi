import time
from .resource import Resource, ClientError
from .common import _create_object
from .regions import Region
from .sizes import Size


class DatabaseConnection:
    """
    This class holds connection information for the database cluster.

    These information can be accessed as attributes.

    Attributes:
        uri (str): 	A connection string in the format accepted by the psql command. This is provided as a convenience and should be able to be constructed by the other attributes.
        database (str): The name of the default database.
        host (str): The FQDN pointing to the database cluster's current primary node.
        port (int): The port on which the database cluster is listening.
        user (str): The default user for the database.
        password (str): The randomly generated password for the default user.
        ssl (bool): A boolean value indicating if the connection should be made over SSL.
    """

    def __init__(self, connection):
        self.__connection = connection
        self.uri = connection["uri"]
        self.database = connection["database"]
        self.host = connection["host"]
        self.port = connection["port"]
        self.user = connection["user"]
        self.password = connection["password"]
        self.ssl = connection["ssl"]

    def __getitem__(self, index):
        return self.__connection[index]

    def __repr__(self):
        return f"<Connection database: {self.database}, user: {self.user}>"

    def json(self):
        return self.__connection


class DatabaseUser:
    """
    A class that represents a user in the database cluster.

    Attributes:
        user (dict): The user object as returned from the API.
        name (str): The name of database user.
        password (str): The password of the database user.
        role (str): A string representing the database user's role. The value will be either "primary" or "normal".
        mysql_settings (dict): An object containing addition configuration details for MySQL clusters

    **mysql_settings** dictionary has this key

    auth_plugin (str): A string specifying the authentication method in use for connections to the MySQL user account. The valid values are "mysql_native_password" or "caching_sha2_password".
    """

    def __init__(self, data):
        self.user = data
        self.name = data["name"]
        try:
            self.mysql_settings = data["mysql_settings"]
        except KeyError:
            pass
        self.password = data["password"]
        self.role = data["role"]

    def __repr__(self):
        return f"<DatabaseUser name: {self.name}, role: {self.role}>"

    def __getitem__(self, index):
        return self.user[index]

    def json(self):
        return self.user


class DatabaseFirewall:
    """
    This class represents a database firewall or inbound source.

    It is used to allow access to the firewall from specific sources
    such as IP addresses, droplets, kubernetes clusters or resources
    tagged with some tag.

    Attributes:
        type (str): The type of resource that the firewall rule allows to access the database cluster. The possible values are: 'droplet', 'k8s', 'ip_addr', or 'tag'
        value (str): The ID of the specific resource, the name of a tag applied to a group of resources, or the IP address that the firewall rule allows to access the database cluster.
    """

    def __init__(self, type, value):
        if not type in ["ip_addr", "droplet", "k8s", "tag"]:
            raise ClientError(
                "Supported types are 'ip_addr', 'droplet', 'k8s', 'tag'")
        self.type = type
        self.value = value

    def json(self):
        return {
            "type": self.type,
            "value": self.value
        }


class DatabaseBackup:
    """
    This class represents a database cluster backup.

    Attributes:
        size_gigabytes (float): The size of the database backup in GBs.
        created_at (datetime.datetime): A time value given in ISO8601 combined date and time format at which the backup was created.
    """

    def __init__(self, created_at, size_gigabytes):
        self.created_at = _create_object("created_at", created_at)
        self.size_gigabytes = size_gigabytes

    def __str__(self):
        return f"<DatabaseBackup size: {self.size_gigabytes} GB, created at: {self.created_at}>"

    def json(self):
        return {
            "size_gigabytes": self.size_gigabytes,
            "created_at": self.created_at
        }


class DatabaseConnectionPool:
    """
    This class represents connection pool for a PostgreSQL database cluster

    Connection pools can be used to allow a database to share its idle connections.

    Attributes:
        name (str): A unique name for the connection pool. Must be between 3 and 60 characters.
        mode (str): The PGBouncer transaction mode for the connection pool. The allowed values are session, transaction, and statement.
        size (int): The desired size of the PGBouncer connection pool. The maximum allowed size is determined by the size of the cluster's primary node. 25 backend server connections are allowed for every 1GB of RAM. Three are reserved for maintenance. For example, a primary node with 1 GB of RAM allows for a maximum of 22 backend server connections while one with 4 GB would allow for 97. Note that these are shared across all connection pools in a cluster.
        db (str): The database for use with the connection pool.
        user (str): The name of the user for use with the connection pool.
        connection (:class:`~dopyapi.databases.DatabaseConnection`): An object containing the information required to access the database using the connection pool.
        private_connection (:class:`~dopyapi.databases.DatabaseConnection`): An object containing the information required to connect to the database using the connection pool via the private network.
    """

    def __init__(self, name, mode, size, db, user, connection=None, private_connection=None):
        if mode not in ["session", "transaction", "statement"]:
            raise ClientError(
                "Only 'session', 'transaction' and 'statement' modes are supported")
        self.name = name
        self.mode = mode
        self.size = size
        self.db = db
        self.user = user
        if isinstance(connection, dict):
            self.connection = DatabaseConnection(connection)
        else:
            self.connection = {}
        if isinstance(private_connection, dict):
            self.private_connection = DatabaseConnection(private_connection)
        else:
            self.private_connection = {}

    def __repr__(self):
        return f"<ConnectionPool name: {self.name}, mode: {self.mode}, size: {self.size}>"

    def json(self):
        return {
            "name": self.name,
            "mode": self.mode,
            "size": self.size,
            "db": self.db,
            "user": self.user,
            "connection": self.connection.json() if self.connection else self.connection,
            "private_connection": self.private_connection.json() if self.private_connection else self.private_connection
        }


class DatabaseCluster(Resource):
    """
    This class represents a single database cluster in Digital Ocean.

    The database cluster simplifies database management, it offers
    these kinds of clusters "PostgreSQL", "MySQL" and "Redis".

    Attributes:
        id (str): A unique ID that can be used to identify and reference a database cluster.
        name (str): A unique, human-readable name referring to a database cluster.
        engine (str): A slug representing the database engine used for the cluster. The possible values are: "pg" for PostgreSQL, "mysql" for MySQL, and "redis" for Redis.
        version (str): A string representing the version of the database engine to use for the cluster. If excluded, the specified engine's default version is used. The available versions for PostgreSQL are "10" and "11" defaulting to the later. For MySQL, the only available version is "8". For Redis, the only available version is "5".
        connection (DatabaseConnection): An object containing the information required to connect to the database (see below).
        private_connection (DatabaseConnection): An object containing the information required to connect to the database via the private network (see below).
        users (list): A list containing objects describing the database's users (see below).
        db_names (list): A list of strings containing the names of databases created in the database cluster.
        num_nodes (int): The number of nodes in the database cluster.
        size (str): The slug identifier representing the size of the nodes in the database cluster.
        region (str): The slug identifier for the region where the database cluster is located.
        status (str): A string representing the current status of the database cluster. Possible values include creating, online, resizing, and migrating.
        maintenance_window (dict): An object containing information about any pending maintenance for the database cluster and when it will occur (see below).
            The used keys for the maintenance windo object are:

            day (str): The day of the week on which to apply maintenance updates (e.g. "saturday").

            hour (str): The hour in UTC at which maintenance updates will be applied in 24 hour format (e.g. "00:22:00").

            pending (bool): A boolean value indicating whether any maintenance is scheduled to be performed in the next window.

            description (list): A list of strings, each containing information about a pending maintenance update.

        created_at (datetime): A time value given in ISO8601 combined date and time format that represents when the database cluster was created.
        tags (list): A list of tags that have been applied to the database cluster.
        private_network_uuid (str): A string specifying the UUID of the VPC to which the database cluster is assigned.

    Connection and Private Connection

    These two dictionaries hold keys and values for connection information,
    used keys are:

            uri (str): A connection string in the format accepted by the psql command. This is provided as a convenience and should be able to be constructed by the other attributes.

            database (str): The name of the default database.

            host (str): The FQDN pointing to the database cluster's current primary node.

            port (int): The port on which the database cluster is listening.

            user (str): The default user for the database.

            password (str): The randomly generated password for the default user.

            ssl (bool): A boolean value indicating if the connection should be made over SSL.
    """
    _url = "databases"
    """
    The URL used for the databases endpoint
    """
    _plural = "databases"
    """
    The dictionary key used when fetching multiple databases
    """
    _single = "database"
    """
    The dictionary key used when fetching a single database
    """
    _fetch_attrs = ["id"]
    """
    These attributes can be used to fetch a database by their value
    """
    _static_attrs = ["connection", "private_connection", "users",
                     "db_names", "status", "maintenance_window", "created_at"]
    """
    These attributes are set by Digital Ocean for a database and cannot be changed directly
    """
    _dynamic_attrs = ["name", "engine", "version", "size",
                      "region", "num_nodes", "tags", "private_network_uuid"]
    """
    These attributes can be used when creating a new database or updating an existing one
    """
    _action_attrs = []
    """
    These are the actions that can be used with the database
    """
    _delete_attr = "id"
    """
    This is the name of the attribute used to delete databases by its value
    """
    _update_attr = "id"
    """
    This is the name of the attribute used to update databases by its value
    """
    _action_attr = ""
    """
    This is the name of the attribute used when calling actions endpoint
    """
    _id_attr = "id"
    """
    This is the name of the attribute used as a Unique Identifier for the resource
    """
    _resource_type = "database"
    """
    This holds the type of resource.
    """

    def __init__(self, data=None):
        super().__init__(DatabaseCluster)
        if data is not None:
            self._update({self._single: data})

    def __repr__(self):
        return f"<Database name: {self.name}>"

    @classmethod
    def list(cls, **kwargs):
        """
        This method returns a list of databases as defined by its arguments

        Arguments:
            page (int): The page to fetch from all databases (defaults 1)
            per_page (int): The number of databases per a single page (defaults 20)

        Returns:
            list: A list of databases
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        databases = super().list(**kwargs)
        return [cls(x) for x in databases]

    def waitReady(self):
        """
        Wait untill the cluster is online, this method
        returns when it is online
        """
        while True:
            if self.status == "online":
                break
            self.load()
            time.sleep(self.ttl)

    def resize(self, size, num_nodes):
        """
        Change the size of the database cluster.

        Args:
            size (str): The new size of the cluster
            num_nodes (int): The new number of nodes
        Return:
            dict : The dictionary response from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = f"{self._url}/{self.id}/resize"
        data = {
            "size": size,
            "num_nodes": num_nodes
        }
        return self.put(url=url, data=data)

    def migrate(self, region):
        """
        Migrate the database cluster to a new region.

        Args:
            region (str): The region to migrate to.
        Return:
            dict : The dictionary response from the API if status code is 204,
                if the status code is 202 it is {"status": "success"}
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = f"{self._url}/{self.id}/migrate"
        data = {
            "region": region
        }
        return self.put(url=url, data=data)

    def createReplica(self):
        """
        Create a new read only replica.

        Args:
            name (str): The name to give the read-only replica.
            region (Region): A slug identifier for the region where the read-only replica will be located. If excluded, the replica will be placed in the same region as the cluster.
            size (str): A slug identifier representing the size of the node for the read-only replica. The size of the replica must be at least as large as the node size for the database cluster from which it is replicating.
            tags (list): A flat list of tag names as strings to apply to the read-only replica after it is created. Tag names can either be existing or new tags.
            private_network_uuid (str): A string specifying the UUID of the VPC to which the read-only replica will be assigned. If excluded, the replica will be assigned to your account's default VPC for the region.
        """
        if self.engine == "redis":
            raise ClientError(
                "Cannot create read only replicas for 'redis' clusters")

    def getReplica(self, name):
        """
        Return a read only replica by its name.

        This method can only be called with mysql and pg clusters

        Args:
            name (str): The name of read only replica
        Return:
            dict : The dictionary response from the API, this dictionary has attributes for ready only replicas.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or when the database cluster engine is redis
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError(
                "Cannot get read only replicas for 'redis' clusters")
        url = f"{self._url}/{self.id}/replicas/{name}"
        return self.get(url=url)["replica"]

    def listReplicas(self):
        """
        Return a list of all read only replicas.

        This method can only be called with mysql and pg clusters

        Return:
            list : A list of read only replica dictionaries, each dictionary has attributes for ready only replicas.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or when the database cluster engine is redis
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError(
                "Cannot list read only replicas for 'redis' clusters")
        url = f"{self._url}/{self.id}/replicas"
        return self.get(url=url)["replicas"]

    def deleteReplica(self, name):
        """
        Delete a read only replica by its name.

        This method can only be called for mysql and pg clusters.
        Args:
            name (str): The name of replica to delete.
        Returns:
            dict: A dictionary with one key "status" and value "deleted" if status code is 204 or 404
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or when the database cluster engine is redis
            ClientForbiddenError : This is raised when the status code is 403
        """
        if self.engine == "redis":
            raise ClientError(
                "Cannot delete read only replicas for 'redis' clusters")
        url = f"{self._url}/{self.id}/replicas/{name}"
        return self.delete(url=url)

    def updateFirewall(self, rules):
        """
        Add a new firewall rule to the database cluster.

        Here we can pass a list of rules or a single rule
        that will be added to the cluster.

        Args:
            rules (list | DatabaseFirewall): A list of rules to add.
        Return:
            dict : The dictionary response from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if not isinstance(rules, list):
            rules = [rules]
        data = []
        for rule in rules:
            data.append({
                "type": rule.type,
                "value": rule.value
            })
        url = f"{self._url}/{self.id}/firewall"
        return self.put(url=url, data={"rules": data})

    def listFirewall(self):
        """
        Return a list of all Firewall rules for the cluster.

        Return:
            list : A list of :class::`~dopyapi.databases.DatabaseFirewall` objects.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or when the database cluster engine is redis
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = f"{self._url}/{self.id}/firewall"
        fws = self.get(url=url)["rules"]
        return [DatabaseFirewall(x) for x in fws]

    def setMaintenanceWindow(self, day, hour):
        """
        Set the maintenance window for the database cluster.

        Here you need to setup two values, one for the day of the week
        and the other is for the hour.

        Args:
            day (str): The day of week for maintenance, for example: 'friday'
            hour (str): The hour of maintenance, for example 23:55
        Return:
            dict : The dictionary response from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = f"{self._url}/{self.id}/maintenance"
        data = {
            "day": day,
            "hour": hour
        }
        return self.put(url=url, data=data)

    def listBackups(self):
        """
        List database backups for the cluster.

        If the cluster is of type 'redis', this will throw :class:`~dopyapi.resource.ClientError`
        exception, otherwise it will return a list of :class:`~dopyapi.databases.DatabaseBackup`
        objects.

        Return:
            list: A list of :class:`~dopyapi.databases.DatabaseBackup` objects.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422, or the
                database cluster type is 'redis'
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError("Cannot list backups for 'redis' clusters")
        url = f"{self._url}/{self.id}/backups"
        backups = self.get(url=url)
        return [DatabaseBackup(**backup) for backup in backups["backups"]]

    def replicate(self, name, size, region=None, tags=[], private_network_uuid=None):
        """
        Replicate the current database cluster to another one, with a different
        name and size.

        If we do not specify a new region then the same region will be
        used for the database cluster.

        Args:
            name(str): The name of the new cluster.
            size (Size): The size of new cluster.
            region (Region): The region for new cluster, default None.
            tags (list): A list of tags for new cluster, default []
            private_network_uuid (str): The UUID of private network for new cluster default is None
        Return:
            dict: The dictionary response from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429, or if the cluster type is redis.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError(
                "Cannot create read only replicas for 'redis' clusters")
        url = f"{self._url}/{self.id}/replicas"
        if region is None:
            region = self.region
        data = {
            "name": name,
            "size": size,
            "region": region,
            "tags": tags,
            "private_network_uuid": private_network_uuid
        }
        return self.post(url=url, data=data)

    def addUser(self, name, auth_plugin="caching_sha2_password"):
        """
        Add a new user to the database cluster.

        Args:
            name (str): The name to give the database user.
            auth_plugin (str): A string specifying the authentication method to be used for connections to the MySQL user account. The valid values are "mysql_native_password" or "caching_sha2_password". If excluded when creating a new user, the default for the version of MySQL in use will be used. As of MySQL 8.0, the default is "caching_sha2_password." default caching_sha2_password
        Return:
            dict: The dictionary response from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429, or the database cluster is of type 'redis' or if authentication plugin is neither 'caching_sha2_password' nor 'mysql_native_password'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError("Cannot create users for redis cluster")
        if auth_plugin not in ["caching_sha2_password", "mysql_native_password"]:
            raise ClientError(
                "Only 'caching_sha2_password' and 'mysql_native_password' authentication plugins are supported")
        mysql_settings = {
            "auth_plugin": auth_plugin
        }
        self.waitReady()
        data = {
            "name": name,
            "mysql_settings": mysql_settings
        }
        return self.post(url=f"{self._url}/{self.id}/users", data=data)

    def getUser(self, name):
        """
        Retrieve information for the database user by name.

        Args:
            name (str): The name of database user to retrieve.
        Return:
            :class:`~dopyapi.databases.DatabaseUser` : An object representing the retrieved user.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or database cluster type is 'redis'
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError("Cannot get users for redis cluster")
        self.waitReady()
        return DatabaseUser(self.get(f"{self._url}/{self.id}/users/{name}")["user"])

    def resetAuth(self, name, auth_plugin):
        """
        Change authentication plugin for the database user.

        This is only available for mysql clusters.

        Args:
            name (str): The name of database user.
            auth_plugin (str): The authentication plugin it could be either 'mysql_native_password' or 'caching_sha2_password'
        Return:
            dict: The dictionary response from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429, or the database cluster type is not 'mysql' or the authentication plugin is neither 'caching_sha2_password' nor 'mysql_native_password'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "mysql":
            if not auth_plugin in ["caching_sha2_password", "mysql_native_password"]:
                raise ClientError(
                    "Only 'mysql_native_password' and 'caching_sha2_password' authentication is supported")
            url = f"{self._url}/{self.id}/users/{name}/reset_auth"
            return self.post(url=url, data={"mysql_settings": {"auth_plugin": auth_plugin}})
        else:
            raise ClientError(
                "Cannot reset auth for 'PostgreSQL' or 'redis' clusters")

    def listUsers(self):
        """
        List all database cluster users.

        Return:
            list : A list of :class:`~dopyapi.databases.DatabaseUser` objects.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or database cluster type is 'redis'
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError("Cannot list users for 'redis' cluster")
        url = f"{self._url}/{self.id}/users"
        users = self.get(url)
        return [DatabaseUser(user) for user in users["users"]]

    def deleteUser(self, name):
        """
        Delete a database user by name.

        Args:
            name (str): The name of database user to delete.
        Returns:
            dict: A dictionary with one key "status" and value "deleted".
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or when the cluster type is 'redis'
            ClientForbiddenError : This is raised when the status code is 403
        """
        if self.engine == "redis":
            raise ClientError("Cannot delete users for 'redis' cluster")
        url = f"{self._url}/{self.id}/users/{name}"
        return self.delete(url=url)

    def addDB(self, name):
        """
        Create a new Database in the cluster.

        Args:
            name (str): The name of new database
        Return:
            dict: The dictionary response from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429 or if the database cluster type is 'redis'
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError(
                "Database management is not supported for 'redis' clusters")
        url = f"{self._url}/{self.id}/dbs"
        return self.post(url, {"name": name})

    def getDB(self, name):
        """
        Retrieve the database from the cluster.

        Args:
            name (str): The name of database to retrieve.
        Return:
            dict : The dictionary response from the API if status code is 200.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is 'redis'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError(
                "Database management is not supported for 'redis' clusters")
        url = f"{self._url}/{self.id}/dbs/{name}"
        return self.get(url)

    def listDBS(self):
        """
        List all databases in the cluster.

        Return:
            list : A list of dictionaries as returned from the API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is 'redis'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine == "redis":
            raise ClientError(
                "Database management is not supported for 'redis' clusters")
        url = f"{self._url}/{self.id}/dbs"
        dbs = self.get(url)
        return [db for db in dbs["dbs"]]

    def deleteDB(self, name):
        """
        Delete a database from the cluster.

        Args:
            name (str): The name of database to delete.
        Returns:
            dict: A dictionary with one key "status" and value "deleted".
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is 'redis'.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if self.engine == "redis":
            raise ClientError(
                "Database management is not supported for 'redis' clusters")
        url = f"{self._url}/{self.id}/dbs/{name}"
        return self.delete(url=url)

    def addPool(self, **kwargs):
        """
        Add a new connection pool to the database cluster if its type is PostgreSQL

        You can pass individual pool attributes here or use
        a :class:`~dopyapi.databases.DatabaseConnectionPool` object.
        """
        if self.engine != "pg":
            raise ClientError(
                "Only PostgreSQL clusters support creating connection pools")
        pool = kwargs.get("pool", None)
        if pool is None:
            pool = DatabaseConnectionPool(**kwargs)
        url = f"{self._url}/{self.id}/pools"
        r = self.post(url=url, data=pool.json())
        return DatabaseConnectionPool(**r["pool"])

    def listPools(self):
        """
        List all connection pools in the cluster.

        Return:
            list : A list of :class:`~dopyapi.databases.DatabaseConnectionPool` objects.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is not 'PostgreSQL'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine != "pg":
            raise ClientError(
                "Listing pools is only available for 'PostgreSQL' clusters")
        url = f"{self._url}/{self.id}/pools"
        pools = self.get(url)
        return [DatabaseConnectionPool(**pool) for pool in pools["pools"]]

    def getPool(self, name):
        """
        Retrieve a connection pool from the cluster.

        Args:
            name (str): The name of the connection pool to retrieve.
        Return:
            :class:`~dopyapi.databases.DatabaseConnectionPool` : The connection pool object.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is not 'PostgreSQL'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine != "pg":
            raise ClientError(
                "Connection Pool management is only available for 'PostgreSQL' clusters")
        url = f"{self._url}/{self.id}/pools/{name}"
        return DatabaseConnectionPool(**self.get(url)["pool"])

    def deletePool(self, name):
        """
        Delete a Connection Pool from the cluster.

        Args:
            name (str): The name of the connection pool to delete.
        Returns:
            dict: A dictionary with one key "status" and value "deleted".
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is not 'PostgreSQL'.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if self.engine != "pg":
            raise ClientError(
                "Connection Pool management is only available for 'PostgreSQL' clusters")
        url = f"{self._url}/{self.id}/pools/{name}"
        return self.delete(url=url)

    def getEvPolicy(self):
        """
        Retrieve the configured eviction policy for an existing Redis cluster.

        Return:
            str : The configured eviction policy.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is not 'Redis'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine != "redis":
            raise ClientError(
                "Eviction Policy can only be used with redis clusters")
        url = f"{self._url}/{self.id}/eviction_policy"
        return self.get(url=url)["eviction_policy"]

    def setEvPolicy(self, policy):
        """
        Set the eviction policy for redis clusters

        Args:
            policy (str): A string specifying the desired eviction policy for the Redis cluster. Valid vaules are: `noeviction`, `allkeys_lru`, `allkeys_random`, `volatile_lru`, `volatile_random`, or `volatile_ttl`.
        Return:
            dict : It returns this dictionary {"status": "success"}
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster's type is not redis.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404

        """
        if self.engine != "redis":
            raise ClientError(
                "Eviction Policy can only be used with redis clusters")
        url = f"{self._url}/{self.id}/eviction_policy"
        return self.put(url=url, data={"eviction_policy": policy})

    def getSqlMode(self):
        """
        Retrieve the configured SQL mode for mysql cluster.

        Return:
            str : A string specifying the configured SQL modes for the MySQL cluster.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster type is not 'mysql'.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if self.engine != "mysql":
            raise ClientError("SQL Mode can only be used with mysql clusters")
        url = f"{self._url}/{self.id}/sql_mode"
        return self.get(url=url)["sql_mode"]

    def setSqlMode(self, mode="ANSI,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,STRICT_ALL_TABLES"):
        """
        Set SQL Mode for mysql clusters

        Args:
            mode (str): A single string specifying the desired SQL modes for the MySQL cluster separated by commas. default is "ANSI,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,STRICT_ALL_TABLES"
        Return:
            dict : It returns this dictionary {"status": "success"}
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422 or if the database cluster's type is not mysql.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404

        """
        if self.engine != "mysql":
            raise ClientError("SQL Mode can only be used with MySQL clusters")
        url = f"{self._url}/{self.id}/sql_mode"
        return self.put(url=url, data={"sql_mode": mode})
