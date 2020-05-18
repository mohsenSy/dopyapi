import requests
import datetime
import logging
from requests_oauthlib import OAuth2

from .auth import Auth
from .common import _create_object

class Resource:
    """
    The base class for all managed Digital Ocean resources

    In this class we have methods to make API requests using HTTP verbs
    (GET, POST, DELETE, HEAD and PUT) which are documented in Digital Ocean
    API documentation, we also use python magic methods to manage
    instance attributes of managed resources.

    Attributes:
        auth (auth.Auth): An authentication object which holds the used access token
            and base URL for all API calls.
        resource (type) : This attribute holds the class of the managed resource,
            this class must extend Resource class and define these class attributes:

            _url: The API endpoint used to manage the resource.

            _single: The dictionary index used when fetching single instances.

            _plural: The dictionary index used when fetching multiple instances.

            _fetch_attrs: A list of attributes that can be used to fetch single instances.

            _static_attrs: A list of attributes set by DO API and cannot be changed directly.

            _dynamic_attrs: A list of attributes that can be changed and saved or used when
            creating new instances.

            _action_attrs: A list of actions that can be used on this resource.

            _delete_attr: An attribute used when deleting instances.

            _update_attr: An attribute used when updating instances.

            _action_attr: An attribute used when calling actions.

            _id_attr: The attribute that hold a unique identifier for the resource.

            _resource_type: The type of resource as a string
    """
    ttl = 10
    def __init__(self, resource):
        self.resource = resource
        self.__dict__["__changed"] = ""
        self.__dict__["__fetched"] = False
        for attr in self.resource._static_attrs:
            self.__dict__[attr] = None
        for attr in self.resource._dynamic_attrs:
            self.__dict__[attr] = None
        for attr in self.resource._fetch_attrs:
            self.__dict__[attr] = None

    def __setattr__(self, attr, value):
        """
        This magic method is called every time an attribute is set.

        If the changed attribute is static nothing is done, if it is dynamic
        it is changed and then the "__changed" attribute is modified.
        """
        if attr == "resource":
            object.__setattr__(self, attr, value)
        resource = object.__getattribute__(self, "resource")
        static_attrs = resource._static_attrs
        dynamic_attrs = resource._dynamic_attrs
        fetch_attrs = resource._fetch_attrs
        if attr in fetch_attrs:
            self.__dict__["__changed"] = attr
            self.__dict__["__fetched"] = False
        if attr in static_attrs:
            return
        self.__dict__[attr] = value
    def __getattribute__(self, attr):
        """
        This magic method is called every time we try to get the value of an attribute.

        If the attribute is in dynamic, static of fetch attributes
        then we try to fetch the instance before we return.
        If the attribute is in action_attrs then we return a lambda function
        that calls the action method with the right type.
        """
        if attr == "resource":
            return object.__getattribute__(self, attr)
        resource = object.__getattribute__(self, "resource")
        static_attrs = resource._static_attrs
        dynamic_attrs = resource._dynamic_attrs
        fetch_attrs = resource._fetch_attrs
        action_attrs = resource._action_attrs
        if attr in static_attrs or attr in dynamic_attrs or attr in fetch_attrs:
            return self.__fetch(attr)
        if attr in action_attrs:
            return lambda **kwargs : self.action(type=attr, **kwargs)
        return object.__getattribute__(self, attr)
    def getID(self):
        """
        Return the ID value for the instance.
        """
        return self.__getattribute__(self.__getattribute__("_id_attr"))
    def __get_dynamic_attrs(self):
        """
        Return a list of dynamic attribute values

        Return:
            list : Dynamic attribute values.
        """
        params = {}
        for attr in self.resource._dynamic_attrs:
            params[attr] = self.__dict__[attr]
        return params
    def save(self, url=None):
        """
        Update the instance with all values for dynamic attributes

        This method calls PUT on the URL for updating the instance, it passes
        all values for dynamic attributes to prevent any loss of any value
        for any attribute.

        Args:
            url (str): The url used to send the update request, if it is None
                then the default URL for the resource is used. default None
        Return:
            dict : The dictionary response from the API if status code is 204.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404

        """
        if self.resource._update_attr == "":
            raise ClientError(f"This resource {self.resource} does not support updating")
        params = self.__get_dynamic_attrs()
        if url is None:
            url = self._url
        self.put(f"{url}/{self.__dict__[self.resource._update_attr]}", params)
    @classmethod
    def __fetch_data(cls, page=1, per_page=20, url=None, **kwargs):
        """
        Fetch a page of resource instances from the API based on url

        Args:
            page (int): The page number to fetch (default is 1)
            per_page (int): The number of instances per a single page (default is 20)
            url (str): The URL to fetch data from it (default is None)
            index (str): The dictionary key used when returning the result,
                it defaults to the pluarl value of used resource.

        Return:
            list : A list of dictionaries for the resource instances.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        resource = Resource(cls)
        res = resource.get(url, page = page, per_page=per_page, **kwargs)
        return res[kwargs.get("index", cls._plural)]
    def __fetch(self, attr):
        """
        Try to fetch from DO API

        If we can fetch single instances from the API then we check
        if we previously fetched from the API if not we fetch using __do_fetch
        method, else we just return the attribute's value

        Args:
            attr (str): The attribute to fetch
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if len(self.resource._fetch_attrs) > 0:
            if self.__dict__["__fetched"] == False:
                return self.__do_fetch(attr)
        return self.__dict__[attr]
    def load(self):
        """
        This method is used to force loading the attributes from the API.

        Returns:
            The value for ID attribute.
        """
        return self.__do_fetch(self._id_attr)
    def __do_fetch(self, attr):
        """
        This function starts a fetch from the API

        It sets __fetched to True and updates the current instance
        based on data received from the API, it returns the attribute's value

        Args:
            attr (str): The attribute to fetch.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        id_attr = object.__getattribute__(self, "_id_attr")
        changed = object.__getattribute__(self, id_attr)
        if self.__dict__['__changed'] != "":
            changed = object.__getattribute__(self, self.__dict__['__changed'])
        if changed is None:
            return None
        res = self.get(f"{self._url}/{changed}")
        self.__fetch_time = datetime.datetime.now()
        self.__dict__["__fetched"] = True
        self._update(res)
        return self.__dict__[attr]
    def _update(self, resource, index=None):
        """
        Here we update instance attributes based on data found in resource dictionary.
        """
        if index is None:
            try:
                res = resource[self._single]
            except Exception as e:
                try:
                    res = resource[self._plural][0]
                except IndexError:
                    return
        else:
            res = resource[index]
        for k, v in res.items():
            if k in self.resource._dynamic_attrs or k in self.resource._static_attrs or k in self.resource._fetch_attrs:
                self.__dict__[k] = _create_object(k, v)
        self.__dict__["__fetched"] = True
    @classmethod
    def list(cls, *args, **kwargs):
        """
        This method is used to fetch multiple instances from the API.

        Args:
            url (str): The URL used for fetching, it defaults to the defined
                URL for the resource.
            page (int): The number of page in results to fetch default is 1
            per_page (int): The number of instances in a single page default is 20
        Returns:
            list: A list of dictionaries from Digital Ocean API.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if kwargs.get("url", None) == None:
            kwargs["url"] = cls._url
        if kwargs.get("page", None) == None:
            kwargs["page"] = 1
        if kwargs.get("per_page", None) == None:
            kwargs["per_page"] = 20
        return cls.__fetch_data(**kwargs)

    def listActions(self, **kwargs):
        """
        This method is used to list all actions for this instance

        Return:
            list : A list of action objects

        Raises:
            ClientError: This is raised if this resource does not support actions
                or the status code is 400 or 422.
            DOError : This is raised when the status code is 500
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if len(self._action_attrs) == 0:
            raise ClientError(f"Cannot list actions for this resource {self.__class__.__name__}")
        from .actions import Action
        id_attr = self.resource.__dict__["_id_attr"]
        return Action.list(url=f"{self._url}/{self.__dict__[id_attr]}/actions", index="actions", **kwargs)

    def getAction(self, action_id):
        """
        This method is used to fetch a single action based on its ID.

        Args:
            action_id (int): The ID of action to fetch.
        Returns:
            Action: The action object with the used ID.
        Raises:
            ClientError: This is raised if this resource does not support actions
                or the status code is 400 or 422.
            DOError : This is raised when the status code is 500
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        if len(self._action_attrs) == 0:
            raise ClientError(f"Cannot get actions for this resource {self.__class__.__name__}")
        from .actions import Action
        action = Action()
        ac = action.get(url=f"{self._url}/{self.__dict__[self._fetch_attrs[0]]}/actions/{action_id}")
        action._update(ac)
        return action
    def json(self):
        """
        Return a dictionary of all Digital Ocean attributes for the resource

        Returns:
            dict: A dictionary of key/value pairs for the object's attributes.
        """
        ret = {}
        self.__fetch(self._id_attr)
        for attr in self.resource._fetch_attrs:
            ret[attr] = object.__getattribute__(self, attr)
        for attr in self.resource._static_attrs:
            ret[attr] = object.__getattribute__(self, attr)
        for attr in self.resource._dynamic_attrs:
            ret[attr] = object.__getattribute__(self, attr)
        return {
            self.resource._single: ret
        }

    def create(self, **kwargs):
        """
        This method is used to create a new instance based on arguments.

        Return:
            dict : JSON object from the API
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        r = self.post(self._url, kwargs)
        self._update(r)
        self.__dict__["__fetched"] = True
        self.__dict__["__fetch_time"] = datetime.datetime.now()
        return r

    def action(self, **kwargs):
        """
        Call an action based on the action_attr and passed arguments

        Args:
            url (str): The url used to call the action, if None then
                the resource's action attribute is used. default None
            tag_name (str): The name of tag to use as a query string. default None
            type (str): The type of action called.

        Return:
            Action : The action just created.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        url = kwargs.get("url", None)
        if url is None:
            url = f"{self.resource._url}/{self.__dict__[self.resource._action_attr]}/actions"
        else:
            del kwargs["url"]
        tag_name = kwargs.get("tag_name", None)
        from .actions import Action
        if tag_name is not None:
            del kwargs["tag_name"]
            action = self.post(url, kwargs, tag_name=tag_name)
            return [Action(action) for action in action["actions"]]
        else:
            action = self.post(url, kwargs)
            return Action(action["action"])

    def __get_json(self, data):
        """
        Update the data object or list by changing objects with their IDs.

        It also changes InboundRule, OutboundRule, Location and ForwardingRule
            objects to their JSON objects, this is helpfull to enable developers
            use objects instead of IDs.
        """
        from .loadbalancers import StickySession, HealthCheck
        for (k,v) in data.items():
            if isinstance(v, Resource):
                data[k] = v.getID()
            elif isinstance(v, list):
                for i in range(len(v)):
                    from .firewalls import InboundRule, OutboundRule, Location
                    from .loadbalancers import ForwardingRule
                    if isinstance(v[i], (InboundRule, OutboundRule, Location, ForwardingRule, StickySession, HealthCheck)):
                        v[i] = v[i].getJSON()
                    if isinstance(v[i], Resource):
                        v[i] = v[i].getID()
            elif isinstance(v, (StickySession, HealthCheck)):
                data[k] = v.getJSON()

    def get(self, url, **kwargs):
        """
        Send a GET request to Digital Ocean API

        Args:
            url (str): The URL to fetch from the API
        Return:
            dict : The dictionary response from the API if status code is 200.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        r = self.__get(url, **kwargs)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 500:
            raise DOError(r.json()["message"])
        if r.status_code == 400 or r.status_code == 422:
            raise ClientError(r.json()["message"])
        if r.status_code == 403:
            raise ClientForbiddenError()
        if r.status_code == 404:
            raise ResourceNotFoundError()

    def __get(self, url, **kwargs):
        """
            Make GET request to the API using the URL with kwargs in query string

            The API GET request is used to fetch data from the API, this could
                be a single object or a list of objects

            Args:
                url (str): The URL to send the request to, this does not include
                    the base url which is automatically added from the stored auth
                    object.
                **kwargs (dictionary): A dictionary of keyword arguments which will
                    be passed in the query string

                Returns:
                    dict: A dictionary of the response.
        """
        token = {
            "access_token": self.auth.token,
            "token_type": "Bearer"
        }
        auth = OAuth2(token=token)
        url = f"{self.auth.base_url}/{url}"
        return requests.get(url, auth=auth, params=kwargs)
    def post(self, url, data, **kwargs):
        """
        Send a POST request to Digital Ocean API

        Args:
            url (str): The URL used when sending the request to the API
        Return:
            dict: The dictionary response from the API if status code is 201 or 202.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400, 422, 409 and 429.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        self.__get_json(data)
        r = self.__post(url, data, **kwargs)
        if r.status_code == 201 or r.status_code == 202:
            return r.json()
        if r.status_code == 500:
            raise DOError()
        if r.status_code == 400 or r.status_code == 422 or r.status_code == 409 or r.status_code == 429:
            raise ClientError(r.json()["message"])
        if r.status_code == 403:
            raise ClientForbiddenError(r.json()["message"])
        if r.status_code == 404:
            raise ResourceNotFoundError(r.json()["message"])

    def __post(self, url, data, **kwargs):
        """
            Make POST request to the API using the URL and data with kwargs in query string

            The API POST request is used to create new objects of resources,
                data dictionary is used to describe the new object, kwargs are
                passed as query string in the URL

            Args:
                url (str): The URL to send the request to, this does not include
                    the base url which is automatically added from the stored auth
                    object.
                data (dictionary): The data sent with the request, it describes
                    the new object to be created
                **kwargs (dictionary): A dictionary of keyword arguments which will
                    be passed in the query string

                Returns:
                    dict: A dictionary of the response.
        """
        token = {
            "access_token": self.auth.token,
            "token_type": "Bearer"
        }
        auth = OAuth2(token=token)
        url = f"{self.auth.base_url}/{url}"
        return requests.post(url, auth=auth, json=data, params=kwargs)
    def put(self, url, data, **kwargs):
        """
        Send a PUT request to Digital Ocean API

        Args:
            url (str): The URL used when sending the request to the API
        Return:
            dict : The dictionary response from the API if status code is 204.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        self.__get_json(data)
        r = self.__put(url, data, **kwargs)
        if r.status_code == 204:
            return r.json()
        if r.status_code == 500:
            raise DOError()
        if r.status_code == 400 or r.status_code == 422:
            raise ClientError(r.json()["message"])
        if r.status_code == 403:
            raise ClientForbiddenError()
        if r.status_code == 404:
            raise ResourceNotFoundError()
    def __put(self, url, data, **kwargs):
        """
            Make PUT request to the API using the URL and data with kwargs in query string

            The API PUT request is used to update objects of resources,
                data dictionary is used to describe the new values, kwargs are
                passed as query string in the URL

            Args:
                url (str): The URL to send the request to, this does not include
                    the base url which is automatically added from the stored auth
                    object.
                data (dictionary): The data sent with the request, it describes
                    the new values for the object to be modified.
                **kwargs (dictionary): A dictionary of keyword arguments which will
                    be passed in the query string

                Returns:
                    dict: A dictionary of the response.
        """
        token = {
            "access_token": self.auth.token,
            "token_type": "Bearer"
        }
        auth = OAuth2(token=token)
        url = f"{self.auth.base_url}/{url}"
        return requests.put(url, auth=auth, json=data, params=kwargs)
    def delete(self, **kwargs):
        """
        Send a DELETE request to Digital Ocean API

        Args:
            url (str): The URL used when sending the request to the API
            data (str): The data to send with the request this is optional and
                it defaults to None.
        Returns:
            dict: A dictionary with one key "status" and value "deleted" if status code is 204 or 404
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422.
            ClientForbiddenError : This is raised when the status code is 403
        """
        if len(kwargs) == 0:
            r = self.__delete(f"{self._url}/{self.__dict__[self._delete_attr]}")
        else:
            url = kwargs.get("url", self._url)
            del kwargs["url"]
            r = self.__delete(f"{url}", **kwargs)
        if r.status_code == 204 or r.status_code == 404:
            return {"status": "deleted"}
        if r.status_code == 500:
            raise DOError()
        if r.status_code == 400 or r.status_code == 422:
            raise ClientError(r.json()["message"])
        if r.status_code == 403:
            raise ClientForbiddenError()
    def __delete(self, url, **kwargs):
        """
            Make DELETE request to the API using the URL with kwargs in query string

            The API DELETE request is used to delete objects of resources,
                kwargs are passed as query string in the URL

            Args:
                url (str): The URL to send the request to, this does not include
                    the base url which is automatically added from the stored auth
                    object.
                **kwargs (dictionary): A dictionary of keyword arguments which will
                    be passed in the query string

                Returns:
                    dict: A dictionary of the resource.
        """
        token = {
            "access_token": self.auth.token,
            "token_type": "Bearer"
        }
        auth = OAuth2(token=token)
        url = f"{self.auth.base_url}/{url}"
        data = kwargs.get("data", None)
        if data is None:
            return requests.delete(url, auth=auth, params=kwargs)
        else:
            del kwargs["data"]
            self.__get_json(data)
            return requests.delete(url, auth=auth, json=data, params=kwargs)
    def head(self, url, **kwargs):
        token = {
            "access_token": self.auth.token,
            "token_type": "Bearer"
        }
        auth = OAuth2(token=token)
        return requests.head(url, auth=auth, params=kwargs)

class ResourceNotFoundError(BaseException):
    """
    This exception is raised when we try to access a URL that does not exist.
    """

class ClientForbiddenError(BaseException):
    """
    This exception is raised when the client is forbidden from accessing Digital Ocean.
    """

class DOError(BaseException):
    """
    This exception is raised when an error happens in Digital Ocean side.
    """

class ClientError(BaseException):
    """
    This exception is raised when the client sends a wrong request
    """
