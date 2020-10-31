
from json import JSONEncoder
from datetime import datetime


def _create_object(name, data):
    """
    Create an object from the returned value in response

        This function is used every time an instance is updated from the API
        This function treats some special cases to create Region, Image, Size
        and datetime objects.

    Args:
        name (str): The index used from the API response
        data (dictionary): This object is usually a dictionary or a string
            and used when creating the object.
    """
    if name == "region":
        from .regions import Region
        if isinstance(data, str):
            return data
        return Region(data)
    if name == "image":
        from .images import Image
        return Image(data)
    if name == "size":
        from .sizes import Size
        if isinstance(data, str):
            return data
        return Size(data)
    if name == "droplet":
        from .droplets import Droplet
        return Droplet(data)
    if name == "inbound_rules":
        from .firewalls import InboundRule
        for index in range(len(data)):
            data[index] = InboundRule(
                data[index]["protocol"], data[index]["ports"], data[index]["sources"])
    if name == "outbound_rules":
        from .firewalls import OutboundRule
        for index in range(len(data)):
            data[index] = OutboundRule(
                data[index]["protocol"], data[index]["ports"], data[index]["destinations"])
    if (name.endswith("_at") or name.startswith("start") or name.startswith("end_") or name == "not_after") and data is not None:
        import datetime
        index = data.find(".")
        if index != -1:
            data = data[:index] + "Z"
        return datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
    if name == "next_backup_window" and isinstance(data, dict):
        import datetime
        data["start"] = datetime.datetime.strptime(
            data["start"], "%Y-%m-%dT%H:%M:%SZ")
        data["end"] = datetime.datetime.strptime(
            data["end"], "%Y-%m-%dT%H:%M:%SZ")
    if name == "latest_tag":
        from .registry import RepositoryTag
        return RepositoryTag(data["registry_name"], data["repository"], data)
    if name == "node_pools":
        from .doks import NodePool
        return [NodePool(**x) for x in data]
    return data


class DOJSONEncoder(JSONEncoder):
    """
    This class is used to encode Digital Ocean resources as JSON objects

    It can be used with `json` module to encode resources.

    It is used as follows::

        with open("droplets.json", "w") as outfile:
            json.dump(data, outfile, cls=do.DOJSONEncoder, sort_keys=True, indent=4)

    Here data is a list that contains objects of Digital Ocean resources.
    """

    def __init__(self, *args, **kwargs):
        super(DOJSONEncoder, self).__init__(*args, **kwargs)

    def default(self, o):
        if hasattr(o, "json"):
            return o.json()
        if isinstance(o, datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)
