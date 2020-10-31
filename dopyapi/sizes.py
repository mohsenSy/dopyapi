"""
This module contains the :class:`~dopyapi.sizes.Size` class to
manage all available sizes in Digital Ocean used when creating
droplets, it also has a set of constants which contain the
values for size slugs, so you do not need to memorize all of
these slugs when creating a new droplet.
"""
from .resource import Resource

t_0_1 = "512mb"
"""
1 vCPU, 512 MB RAM
"""
s_1_1 = "s-1vcpu-1gb"
"""
1 vCPU, 1 GB RAM
"""
t_1_1 = "1gb"
"""
1 vCPU, 1 GB RAM
"""
s_1_2 = "s-1vcpu-2gb"
"""
1 vCPU, 2 GB RAM
"""
s_1_3 = "s-1vcpu-3gb"
"""
1 vCPU, 3 GB RAM
"""
s_2_2 = "s-2vcpu-2gb"
"""
2 vCPU, 2 GB RAM
"""
s_3_1 = "s-3vcpu-1gb"
"""
3 vCPU, 1 GB RAM
"""
t_2_2 = "2gb"
"""
2 vCPU, 2 GB RAM
"""
s_2_4 = "s-2vcpu-4gb"
"""
2 vCPU, 4 GB RAM
"""
t_2_4 = "4gb"
"""
2 vCPU, 4 GB RAM
"""
s_4_8 = "s-4vcpu-8gb"
"""
4 vCPU, 8 GB RAM
"""
m_1_8 = "m-1vcpu-8gb"
"""
1 vCPU, 8 GB RAM
"""
c_2_4 = "c-2"
"""
2 vCPU, 4 GB RAM
"""
g_2_8 = "g-2vcpu-8gb"
"""
2 vCPU, 8 GB RAM
"""
gd_2_8 = "gd-2vcpu-8gb"
"""
2 vCPU, 8 GB RAM
"""
m_2_16 = "m-16gb"
"""
2 vCPU, 16 GB RAM
"""
s_6_16 = "s-6vcpu-16gb"
"""
6 vCPU, 16 GB RAM
"""
c_4_8 = "c-4"
"""
4 vCPU, 8 GB RAM
"""
t_4_8 = "8gb"
"""
4 vCPU, 8 GB RAM
"""

tiny = "s-1vcpu-1gb"
"""
A tiny size, 1vCPU, 1 GB RAM
"""
small = "s-1vcpu-3gb"
"""
A small size, 1vCPU, 3 GB RAM
"""
medium = "s-2vcpu-4gb"
"""
A medium size, 2vCPU, 4 GB RAM
"""
big = "s-4vcpu-8gb"
"""
A big size, 4vCPU, 8 GB RAM
"""
large = "s-6vcpu-16gb"
"""
A large size, 6vCPU, 16 GB RAM
"""

db_1_1 = "db-s-1vcpu-1gb"
"""
Database size: 1 vCPU 1 GB RAM, 10 GB HD
"""
db_1_2 = "db-s-1vcpu-2gb"
"""
Database size: 1 vCPU 2 GB RAM, 25 GB HD
"""
db_2_4 = "db-s-2vcpu-4gb"
"""
Database size: 2 vCPU 4 GB RAM, 38 GB HD
"""
db_4_8 = "db-s-4vcpu-8gb"
"""
Database size: 4 vCPU 8 GB RAM, 115 GB HD
"""
db_6_16 = "db-s-6vcpu-16gb"
"""
Database size: 6 vCPU 16 GB RAM, 270 GB HD
"""
db_8_32 = "db-s-8vcpu-32gb"
"""
Database size: 8 vCPU 32 GB RAM, 580 GB HD
"""
db_16_64 = "db-s-16vcpu-64gb"
"""
Database size: 16 vCPU 64 GB RAM, 1.12 TB HD
"""

db_tiny = db_1_1
"""
Tiny database size : 1 vCPU 1 GB RAM, 10 GB HD
"""
db_small = db_1_2
"""
Small database size : 1 vCPU 2 GB RAM, 25 GB HD
"""
db_medium = db_2_4
"""
Medium database size : 2 vCPU 4 GB RAM, 38 GB HD
"""
db_large = db_4_8
"""
Large database size : 4 vCPU 8 GB RAM, 115 GB HD
"""
db_xlarge = db_6_16
"""
X large database size : 6 vCPU 16 GB RAM, 270 GB HD
"""
db_xxlarge = db_8_32
"""
XX large database size : 8 vCPU 32 GB RAM, 580 GB HD
"""
db_xxxlarge = db_16_64
"""
XXX large database size : 16 vCPU 64 GB RAM, 1.12 TB HD
"""


class Size(Resource):
    """
    This class represents sizes in DO which are used when creating droplets.

    A size includes the amount of RAM, Virtual CPUs, disk and transfer available
    for a droplet once created using it.

    Attributes:
        slug (str): A human-readable string that is used to uniquely identify each size.
        available (bool): Whether this size is available for droplet creation or not.
        transfer (float): The amount of bandwidth transfer available for droplets of this size.
        price_monthly (float): The monthly cost for this size in US dollars.
        price_hourly (float): The hourly cost for this size in US dollars.
        memory (int): The RAM available for this size.
        vcpus (int): The Virtual CPUs available for this size.
        disk (int): The amount of disk space available for this size.
        regions (list): A list containing the region slugs where this size is available for Droplet creates.
    """

    _url = "sizes"
    """
    The API endpoint for sizes.
    """
    _plural = "sizes"
    """
    The dictionary index used when fetching multiple size instances.
    """
    _single = "size"
    """
    The dictionary index used when fetching single size instance.
    """
    _fetch_attrs = []
    """
    The attributes that can be used to fetch size instances.
    """
    _dynamic_attrs = []
    """
    The attribute that can be changed on sizes.
    """
    _static_attrs = ["slug", "available", "transfer", "price_monthly",
                     "price_hourly", "regions", "memory", "vcpus", "disk"]
    """
    Size attributes that cannot be changed.
    """
    _action_attrs = []
    """
    List of size defined actions.
    """
    _delete_attr = ""
    """
    The attribute used when deleting a size.
    """
    _update_attr = ""
    """
    The attribute used when updating a size.
    """
    _action_attr = ""
    """
    The attribute used when calling actions.
    """
    _id_attr = "slug"
    """
    The name of attribute used as an ID for sizes.
    """

    def __init__(self, data=None):
        super().__init__(Size)
        if data is not None:
            self._update({self._single: data})

    def __repr__(self):
        return f"<Size slug: {self.slug}>"

    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of size instances.

        Args:
            page (int): The page we want to fetch. (default 1)
            per_page (int): The number of size instances in a single page. (default 20)

        Return:
            list : A list of sizes instances.
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        sizes = super().list(**kwargs)
        return [cls(size) for size in sizes]
