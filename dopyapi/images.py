"""
This module is contains the :class:`~dopyapi.images.Image` class
to manage images in Digital Ocean, it also has some constants that
contain the slug values for the most popular images in Digital Ocean,
so you do not have to memorize all the image slugs.
"""
import datetime

from .resource import Resource

# Constants for images and their slugs
ubuntu_14_04_32="ubuntu-14-04-x32"
"""
Ubuntu 14.04 32 bit image
"""
ubuntu_14_04_64="ubuntu-14-04-x64"
"""
Ubuntu 14.04 64 bit image
"""
ubuntu_16_04_32="ubuntu-16-04-x32"
"""
Ubuntu 16.04 32 bit image
"""
ubuntu_16_04_64="ubuntu-16-04-x64"
"""
Ubuntu 16.04 64 bit image
"""
ubuntu_18_04_64="ubuntu-18-04-x64"
"""
Ubuntu 18.04 64 bit image
"""
ubuntu_19_10_64="ubuntu-19-10-x64"
"""
Ubuntu 19.10 64 bit image
"""

ubuntu="ubuntu-18-04-x64"
"""
This creates an Ubuntu 18.04 image by default.
"""

debian_9_64="debian-9-x64"
"""
Debian 9 64 bit
"""
debian_10_64="debian-10-x64"
"""
Debian 10 64 bit
"""

debian="debian-10-x64"
"""
Default debian image, 10 64 bit.
"""

freebsd_10_4_64_zfs="freebsd-10-4-x64-zfs"
"""
FreeBSD 10.4 64 bit with ZFS
"""
freebsd_10_4_64="freebsd-10-4-x64"
"""
FreeBSD 10.4 64 bit
"""
freebsd_11_64_ufs="freebsd-11-x64-ufs"
"""
FreeBSF 11 64 bit with UFS
"""
freebsd_11_64_zfs="freebsd-11-x64-zfs"
"""
FreeBSF 11 64 bit with ZFS
"""
freebsd_12_64="freebsd-12-x64"
"""
FreeBSF 12 64 bit
"""
freebsd_12_64_zfs="freebsd-12-x64-zfs"
"""
FreeBSF 12 64 bit with ZFS
"""

freebsd="freebsd-12-x64"
"""
Default FreeBSD image, 12 with 64 bit
"""

fedora_27_64="fedora-27-x64"
"""
Fedora 27 64 bit
"""
fedora_28_64="fedora-28-x64"
"""
Fedora 28 64 bit
"""
fedora_28_64_atomic="fedora-28-x64-atomic"
"""
Fedora 28 64 bit, atomic
"""
fedora_30_64="fedora-30-x64"
"""
Fedora 30 64 bit
"""

fedora="fedora-30-x64"
"""
Default fedora 30 with 64 bit
"""

centos_6_32="centos-6-x32"
"""
CentOS 6, 32 bit
"""
centos_6_64="centos-6-x64"
"""
CentOS 6, 64 bit
"""
centos_7_64="centos-7-x64"
"""
CentOS 7, 64 bit
"""
centos_8_64="centos-8-x64"
"""
CentOS 8, 64 bit
"""
centos_8_32="centos-8-x32"
"""
CentOS 8, 32 bit
"""

centos="centos-8-x64"
"""
Default centos, 8 with 64 bit
"""

rancheros="rancheros"
"""
RancherOS
"""
coreos_alpha="coreos-alpha"
"""
CoreOS alpha
"""
coreos_beta="coreos-beta"
"""
CoreOS beta
"""
coreos_stable="coreos-stable"
"""
CoreOS stable
"""
caprover_18_04="caprover-18-04"
"""
CapRover with Ubuntu 18.04
"""
skaffolder_18_04="skaffolder-18-04"
"""
Skaffolder with Ubuntu 18.04
"""
gitea_18_04="gitea-18-04"
"""
GitEA with Ubuntu 18.04
"""
cassandra="cassandra"
"""
Cassandra
"""
docker="docker-18-04"
"""
Docker on Ubuntu 18.04
"""

class Image(Resource):
    """
    This class represents a single Image in Digital Ocean

    This class is used to manage Images in Digital Ocean, it has methods
    to list all available images, create and delete images too.

    Attributes:
        id (int): A numberic ID for the image used in Digital Ocean to identify the image defaults (None)
        name (str): A human readable name for the image used in User Interfaces. defaults (None)
        type (str): The type of the image it could be one of the following ("snapshot", "backup", "custom") defaults (None)
        distribution (str): Here we store the base distribution used in the image. defaults (None)
        slug (str): A unique string that identifies the image. defaults (None)
        public (bool): This checks if the image is public or not. defaults (None)
        regions (list): An array of regions where this image is available. defaults (None)
        min_disk_size (int): The minimum size in gigabytes needed to create a droplet of this image. defaults (None)
        size_gigabytes (float): The size of the image in gigabytes. defaults (None)
        description (str): A description of the image. defaults (None)
        tags ([]): A list of tags for the image. defaults (None)
        status (str): This string indicates the status of a custom image, it could have one of these values ("NEW", "available", "pending", "deleted"). defaults (None)
        error_message (str): An error image for the custom image. defaults (None)
    Supported actions:
        You call these actions as methods on :class:`~dopyapi.images.Image`
        and return :class:`~dopyapi.actions.Action` objects

        transfer: This is used to transfer an image to another region, it takes one argument called ``region``, it could be the regionss slug or a :class:`~dopyapi.regions.Region` object.

        convert: This is used to convert an image to a snapshot.

    """
    _url = "images"
    """
    The url used for the images endpoint
    """
    _plural = "images"
    """
    The dictionary index used when fetching multiple images
    """
    _single = "image"
    """
    The dictionary index used when fetching single image
    """
    _fetch_attrs = ["id", "slug"]
    """
    A list of attributes that can be used to fetch images based on them.
    """
    _dynamic_attrs = ["name", "distribution", "description"]
    """
    A list of attributes that can be used when creating or updating a new image
    """
    _static_attrs = ["type", "public", "regions", "created_at", "min_disk_size", "size_gigabytes", "tags", "status", "error_message"]
    """
    A list of attributes that are set by Digital Ocean and cannot be changed directly.
    """
    _action_attrs = ["transfer", "convert"]
    """
    A list of actions for images.
    """
    _delete_attr = "id"
    """
    The attribute used when deleting an image
    """
    _update_attr = "id"
    """
    The attribute used when updating an image.
    """
    _action_attr = "id"
    """
    The attribute used when calling actions, no actions here.
    """
    _resource_type = "image"
    """
    The type of resource, it is used when tagging resources.
    """
    _id_attr = "id"
    """
    The attribute used as a unique identifier for the image
    """
    def __init__(self, data=None):
        super().__init__(Image)
        if data is not None:
            self._update({self._single: data})
    def __repr__(self):
        if self.slug is not None:
            return f"<Image slug: {self.slug}>"
        return f"<Image id: {self.id}>"
    def __str__(self):
        if self.slug is not None:
            return self.slug
        return str(self.id)
    @classmethod
    def list(cls, **kwargs):
        """
        Return a list of images based on arguments

        Arguments:
            page (int): The page to fetch (defaults 1)
            per_page (int): The number of images in the page (defaults 20)
        Return:
            list: A list of image objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        images = super().list(**kwargs)
        return [cls(image) for image in images]
    @classmethod
    def listDistribution(cls, **kwargs):
        """
        Return a list of distribution images

        Arguments:
            page (int): The page to fetch (defaults 1)
            per_page (int): The number of images in the page (defaults 20)
        Return:
            list: A list of image objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(type="distribution", **kwargs)

    @classmethod
    def listApplication(cls, **kwargs):
        """
        Return a list of application images

        Arguments:
            page (int): The page to fetch (defaults 1)
            per_page (int): The number of images in the page (defaults 20)
        Return:
            list: A list of image objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(type="application", **kwargs)
    @classmethod
    def listUser(cls, **kwargs):
        """
        Return a list of user private images

        Arguments:
            page (int): The page to fetch (defaults 1)
            per_page (int): The number of images in the page (defaults 20)
        Return:
            list: A list of image objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(private="true", **kwargs)
    @classmethod
    def listByTag(cls, tag_name, **kwargs):
        """
        Return a list of images that match the tag

        Arguments:
            tag_name (str): The name of the tag for the images
            page (int): The page to fetch (defaults 1)
            per_page (int): The number of images in the page (defaults 20)
        Return:
            list: A list of image objects
        raises:
            DOError : This is raised when the status code is 500
            ClientError : This is raised when the status code is 400 or 422
            ClientForbiddenError : This is raised when the status code is 403
            ResourceNotFoundError : This is raised when the status code is 404
        """
        return cls.list(tag_name=tag_name, **kwargs)

class Distribution(object):
    """
    This class could be used when creating a new private image to specify
    the distribution for the image.
    """
    ubuntu = "Ubuntu"
    """
    Ubuntu
    """
    arch_linux = "Arch Linux"
    """
    Arch Linux
    """
    centos = "CentOS"
    """
    CentOS
    """
    coreos = "CoreOS"
    """
    CoreOS
    """
    debian = "Debian"
    """
    Debian
    """
    fedora = "Fedora"
    """
    Fedora
    """
    fedora_atomic = "Fedora Atomic"
    """
    Fedora atomic
    """
    freebsd = "FreeBSD"
    """
    FreeBSD
    """
    gentoo = "Gentoo"
    """
    Gentoo
    """
    opensuse = "openSUSE"
    """
    OpenSUSE
    """
    rancheros = "RancherOS"
    """
    RancherOS
    """
