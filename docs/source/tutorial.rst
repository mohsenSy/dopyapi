========
Tutorial
========

In this tutorial we will give examples to the usage of all defined resources
so far, new sections will be added to every new resource.

.. note::
  To follow along in all sections here make sure to import the library
  and authenticate using this code::

    import dopyapi as do
    do.authenticate()

List all available regions, images and sizes
--------------------------------------------

When you create Digital Ocean resource, every resource need to be associated
with a region, where Digital Ocean data centers exist, there are 9 regions
in Digital Ocean they can be fetched using this code::

  regions = do.Region.list()
  for region in regions:
    print(region)

The previous code prints all available regions, when you print a Digital
Ocean resource object it prints the name of class along with one or two
attributes that help you to identify the resource.

An image is used when creating new droplets, it specifies the Operating
System found in the droplet when created, the :mod:`~dopyapi.images`
module contains constants for the most popular image names.

To list images use this code::

  images = do.Image.list()
  for image in images:
    print(image)

There are other methods for listing images these are :meth:`~dopyapi.images.Image.listDistribution`,
:meth:`~dopyapi.images.Image.listApplication`,:meth:`~dopyapi.images.Image.listUser` and :meth:`~dopyapi.images.Image.listByTag`.

When creating droplets we can use the image's object or the image's slug, this
will be described later.

Now for tor the sizes, the size of a droplet defines how much resources will
be allocated for it such as CPU, RAM and Disk, each droplet will have size
associated with it, you can use size objects or sizes slugs which are
provided as constants in :mod:`~dopyapi.sizes` module.

The following code lists some available sizes::

  sizes = do.Size.list()
  for size in sizes:
    print(size)

List SSH Keys and tags
----------------------
To list all available SSH keys in your account use this code::

  ssh_keys = do.SSHKey.list()
  for ssh_key in ssh_keys:
    print(ssh_key)

Tags are associated with resources to help us group similar resources
together, if we specify a tag for a new resource and this tag does not
exist it is automatically created for us by Digital Ocean.

The following code shows how to list tags::

  tags = do.Tag.list()
  for tag in tags:
    print(tag)

To create a new tag use this code::

  tag = do.Tag()
  tag.create(name="web-backend")

You can also check all the resources tagged with ``web-backend`` for example
using this code::

  tag = do.Tag()
  tag.name = "web-backend"
  print(tag.resources)

Here we get a dictionary that contains an attribute for each resource
that can be tagged along with counts, an example value is shown bellow::

  "resources": {
    "count": 5,
    "last_tagged_uri": "https://api.digitalocean.com/v2/images/7555620",
    "droplets": {
      "count": 1,
      "last_tagged_uri": "https://api.digitalocean.com/v2/droplets/3164444"
    },
    "images": {
      "count": 1,
      "last_tagged_uri": "https://api.digitalocean.com/v2/images/7555620"
    },
    "volumes": {
      "count": 1,
      "last_tagged_uri": "https://api.digitalocean.com/v2/volumes/3d80cb72-342b-4aaa-b92e-4e4abb24a933"
    },
    "volume_snapshots": {
      "count": 1,
      "last_tagged_uri": "https://api.digitalocean.com/v2/snapshots/1f6f46e8-6b60-11e9-be4e-0a58ac144519"
    },
    "databases": {
      "count": 1,
      "last_tagged_uri": "https://api.digitalocean.com/v2/databases/b92438f6-ba03-416c-b642-e9236db91976"
    }
  }

Create a new droplet
--------------------

To create a new droplet we need the following:

* name: The name of the droplet.
* image: The image used in the droplet, this could be a slug or :class:`~dopyapi.images.Image` object.
* size: The size used in the droplet, this could be a slug or :class:`~dopyapi.sizes.Size` object.
* region: The region where the droplet will be created, this could be the region's name or an object of :class:`~dopyapi.regions.Region`
* ssh_keys: A list of SSH keys to insert into the droplet, this is optional,
  you can use either the IDs of keys or :class:`~dopyapi.sshkeys.SSHKey` object, this is passed as a list.

Use this code to create the droplet::

  droplet = do.Droplet()
  droplet_data = {
    "name": "d1",
    "image": do.images.ubuntu,
    "region": "ams3",
    "size": do.sizes.small,
    "ssh_keys": do.SSHKey.list()
  }
  droplet.create(**droplet_data)

Droplet actions can be called using methods with the same as action name,
and use the same parameters as the action, you can find details
in the :class:`~dopyapi.droplets.Droplet` API.

Create and list firewalls
-------------------------

To list firewalls use this code::

  fws = do.Firewall.list()
  for fw in fws:
    print(fw)

We have shown previously here :ref:`create_firewall` how to create firewalls.

Create and list Block Storage volumes
-------------------------------------

To create a block storage volume we need to specify three required attributes:

* name: The name of the volume.
* size_gigabytes: The size of the volume in Giga Bytes.
* region: The region slug where the volume will be created, you
  can also use a :class:`~dopyapi.regions.Region` object.
* description: This text could be used to describe the volume, it is optional.
* tags: A list of tags to assign to the volume, it could consist
  of tag names or :class:`~dopyapi.tags.Tag` objects, it is optional.

Use this code to create a new tag::

  volume = do.Volume()
  volume_data = {
    "name": "v1",
    "region": "ams3",
    "size_gigabytes": 10,
    "tags": ["db_data"],
    "description": "Store database files"
  }
  volume.create(**volume_data)

To list volumes use this code::

  volumes = do.Volume.list()
  for volume in volumes:
    print(volume)

To take a volume snapshot, use this code::

  snapshot = volume.snapshot(name="s1")
  print(snapshot)

To attach a volume to a droplet use this code::

  volume.attach(droplet_id = droplet)

Create and list load balancers
------------------------------

To create a new load balancer we must prepare these attributes:

* name: The name of the load balancer.
* region: The region slug where the load balancer will be created,
  you can also use the :class:`~dopyapi.regions.Region` object.
* forwarding_rules: A list of :class:`~dopyapi.loadbalancers.ForwardingRule`,
  each of these objects defines how will the load balancer forward traffic to backend
  droplets, at least one rule shoul exist.
* sticky_sessions: An object of :class:`~dopyapi.loadbalancers.StickySession`, which
  specifies how sessions are handled, this is optional.
* health_check: An object of :class:`~dopyapi.loadbalancers.HealthCheck`, which
  specifies how backend droplets are checked for their health, this is optional.
* redirect_http_to_https: A boolean value that determines if HTTP traffic
  will be redirected to HTTPS by the laod balancer, this defaults to False.

To create a load balancer, use this code::

  lb = do.LoadBalancer()
  forwarding_rule = do.ForwardingRule()
  forwarding_rule.entry_protocol = "http"
  forwarding_rule.entry_port = 80
  forwarding_rule.target_protocol = "http"
  forwarding_rule.target_port = 80
  sticky_session = do.StickySession()
  sticky_session.type = "cookies"
  sticky_session.cookie_name = "lb-do"
  health_check = do.HealthCheck()
  health_check.protocol = "http"
  health_check.port = 80
  health_check.path = "/check"
  lb_data = {
    "name": "lb1",
    "region": "ams3",
    "forwarding_rules": [forwarding_rule],
    "sticky_sessions": sticky_session,
    "health_check": health_check
  }
  lb.create(**lb_data)

Here we used an object of :class:`~dopyapi.loadbalancers.ForwardingRule`
to create a single forwarding_rule and passed a list to the create method,
we created an object of :class:`~dopyapi.loadbalancers.StickySession`
to use cookie based sessions, with cookie name set to "lb-do", and lastly
we used the :class:`~dopyapi.loadbalancers.HealthCheck` class to tell
the load balancer to use the path `/check` for health checks instead of
`/` default.

Create a floating IP and assign it to a droplet
-----------------------------------------------

To create floating IPs we need one of these two:

* A droplet id to assign the IP to it.
* A region slug or :class:`~dopyapi.regions.Region` object
  to reserve the IP for the used region.

Check this code for both methods to create IPs::

  fp_droplet = do.FloatingIP()
  fp_droplet.create(droplet_id = droplet)
  fp_region = do.FloatingIP()
  fp_region.create(region="ams3")

Assigning a floating IP to a droplet is done using the assign method::

  ac = fp_region.assign(droplet_id = droplet)
  print(ac)

Here ``ac`` is an :class:`~dopyapi.actions.Action` object.

Retrieve Balance and Billing information
----------------------------------------

To get your current available balance use the :class:`~dopyapi.bills.Balance`
class, and to get your bills use the :class:`~dopyapi.bills.BillingHistory`
class as follows::

  balance = do.Balance()
  print(balance.json())
  bills = do.BillingHistory.list()
  for bill in bills:
  print(bill.json())

Create and transfer custom images
--------------------------------------
You can create custom private images in Digital Ocean, use
this code to create a custom image with a minimal Ubuntu 18.04
pre-installed::

  image = do.Image()
  image_data = {
    "name": "ubuntu-18-04-minimal",
    "url": "http://cloud-images.ubuntu.com/minimal/releases/bionic/release/ubuntu-18.04-minimal-cloudimg-amd64.img",
    "distribution": do.images.Distribution.ubuntu,
    "region": "ams3",
    "description": "A minimal Ubuntu 18.04 installation",
    "tags": ["custom-image"]
  }
  image.create(**image_data)

After the image is created we can find it using :meth:`~dopyapi.images.Image.listUser`
method as shown bellow::

  images = do.Image.listUser()
  for image in images:
    print(image)

To transfer this image we can use this code::

  images = do.Image.listUser()
  for image in images:
    if image.name == "ubuntu-18-04-minimal":
        action = image.transfer(region="nyc3")
        print(action)

Create and List VPCs
--------------------

You can use the :class:`~dopyapi.vpcs.VPC` class to manage VPCs
on Digital Ocean, the list class method is used to list all VPCs,
to create a new VPC you can use this code::

  vpc = do.VPC()
  vpc_data = {
    "name": "ams3-vpc",
    "region": "ams3",
    "description": "A new VPC in ams3"
  }
  vpc.create(**vpc_data)

In the previous code we did not specify an IP range for the VPC, it was
selected automatically by Digital Ocean for us, we can specify our own
IP range with adding ``ip_range`` key to the request, however we must
make sure that the range is unique within our account and also
must not be smaller than ``/24`` or larger that ``/16``.
