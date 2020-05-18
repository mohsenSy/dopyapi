===============
Getting Started
===============

We will explain here the basic usage of :program:`dopyapi`, using simple code.

Get an access token
-------------------

Before you start using the library you must acquire an access token
from your Digital Ocean account, to get one visit this `URL`_, click
on ``Generate New Token`` then save the token you see somewhere safe
and make sure to keep it because you will not be able to see it again.

Export the ``DO_TOKEN`` variable in your shell session to be able
to use it later in the code::

  export DO_TOKEN=<access token>

Print Account Information
-------------------------

The following code prints user information in JSON format, notice we did
not pass any value to ``do.authenticate()`` because it will use the value
stored in *DO_TOKEN* when we do not pass any value to it::

  import dopyapi as do
  do.authenticate()
  account = do.Account()
  print(account.json())

Every class for a  Digital Ocean has the ``json`` method to return a dictionary
that contains all attributes for that resource with their values.

You can print account information individually like this::

  print(account.email) # Print user email
  print(account.droplet_limit) # Print how many droplets can a user create

List all available droplets
---------------------------

Now let us try to list all available droplets::

  droplets = do.Droplet.list()
  for droplet in droplets:
    print(droplet)

Each resource in Digital Ocean is represented by a class whose name starts
with a capital letter and is singular, and all these classes has the ``list``
method that returns a list of objects for this resource, this method takes
these two shared parameters:

* page: The number of page to fetch resources from it, default is 1
* per_page: The number of resources returned, default is 20

Create a new droplet
--------------------

To create a new droplet use this code::

  droplet = do.Droplet()
  droplet_data = {
    "name": "droplet1",
    "image": do.images.ubuntu,
    "size": do.sizes.tiny,
    "region": "ams3"
  }
  droplet.create(**droplet_data)
  print(droplet.getPublicIP())

In this code we created a new object of :class:`~dopyapi.droplets.Droplet`, then we prepared
a dictionary to hold the values of attributes that will be used when creating
the droplet, then we call the method :meth:`~dopyapi.resource.Resource.create`, this method is used by all
classes to create new resources.

Lastly we use the method :meth:`~dopyapi.droplets.Droplet.getPublicIP` to print the public IP address of the
new droplet, this method will wait untill the droplet is ready.

Take snapshot of a Droplet
--------------------------

In Digital Ocean API, taking a Droplet snapshot is considered as an action, and
here in our library we have methods for each action associated with a resource
that has the same action's name and takes named parameters, and returns an action
object, the following code takes a snapshot of a droplet and uses the returned
action object to wait until the snapshot is finished::

  droplets = do.Droplet.list()
  droplet = droplets[0]
  action = droplet.snapshot(name="s1")
  while action.status == "in-progress":
    action.load()
  if action.status == "completed":
    print("snapshot was finished successfully")
  else:
    print("There was an error with snapshot")

In the previous code we fetch a list of droplets first, then we take
the first droplet from the list and call the method ``snapshot`` on it.

Then we use a while loop and check the status of the action until it is not
in-progress anymore, after that if the status was "completed" we print a
success message and if it was not "completed" we print an error message.

.. note::
  Notice that the ``snapshot`` method does not have a link to a method
  in the class :class:`~dopyapi.droplets.Droplet`, that is because we use
  python's magic methods to implement actions and many more features here,
  you can learn more about our use of magic methods in :doc:`magic_methods`

List Droplet snapshots
----------------------

To list the snapshots of a droplet use this code::

  snapshots = droplet.listSnapshots()
  for snapshot in snapshots:
    print(snapshot)

Here every element of the list is an instance of :class:`~dopyapi.snapshots.Snapshot`.

.. _create_firewall:

Create a new firewall and assign it to a droplet
------------------------------------------------

To create a firewall we need to prepare objects of :class:`~dopyapi.firewalls.Location`,
:class:`~dopyapi.firewalls.InboundRule` and :class:`~dopyapi.firewalls.OutboundRule`.

The following code shows how to do it::

  location_local = do.Location(addresses=["192.168.2.0/24"]) # This defines a location that matches all IP addresses in subnet "192.168.2.0/24"
  location_all = do.Location(addresses=["0.0.0.0/0"])
  inbound_rule = do.InboundRule(ports="1234", protocol="udp", sources=location_local) # this defines an inbound rule for protocol udp and port 1234 using the previous location as source of traffic
  outbound_rule = do.OutboundRule(destinations=location_all) # This defines an outbound rule that matches all tcp traffic to all ports and destinations
  firewall = do.Firewall()
  firewall.create(name="fw1", inbound_rules=[inbound_rule], outbound_rules=[outbound_rule])
  droplets = do.Droplet.list()
  firewall.addDroplets(droplets[0])

In the previous code we used two objects of :class:`~dopyapi.firewalls.Location`, to hold
the addresses of a local subnet and also all available addresses, the first one is used
to allow traffic from local network and the other to allow traffic to all addresses.

We also used two objects of :class:`~dopyapi.firewalls.InboundRule` and :class:`~dopyapi.firewalls.OutboundRule`
to add two rules to our firewall, then we declared an object of class :class:`~dopyapi.firewalls.Firewall`
and used the :meth:`~dopyapi.firewalls.Firewall.create` method to create the firewall.

Then we retrieved a list of Digital Ocean droplets and assigned the
firewall to the first droplet.

List and create SSH keys
------------------------

In order to list all available SSH keys you need to use the :meth:`~dopyapi.sshkeys.SSHKey.list`
method just like all other resources that has this method available::

  ssh_keys = do.SSHKey.list()
  for ssh_key in ssh_keys:
    print(ssh_key)

To create an SSH key we need to specify its name and public key as follows::

  import os
  ssh_key = do.SSHKey()
  public_key = open(f"{os.environ['HOME']}/.ssh/id_rsa.pub", "r").read()
  ssh_key_data = {
    "name": "new-key",
    "public_key": public_key
  }
  ssh_key.create(**ssh_key_data)

You need to have a public key available at ``~/.ssh/id_rsa.pub`` and also
this public must not exist in your account or you will get :class:`~dopyapi.resource.ClientError`
with this message ``SSH Key is already in use on your account``.

List images
-----------

Use the following code to list available images::

  images = do.Image.list(page=2, per_page=30)
  for image in images:
    print(image)
  user_images = do.Image.listUser()
  for image in user_images:
    print(image)
  app_images = do.Image.listApplication()
  for image in app_images:
    print(image)

The previous code uses the ``page`` and ``per_page`` parameters to choose
the page of images to fetch from the API, here we are fetching the second
30 images instead of the first 20 by default, we also used :meth:`~dopyapi.images.Image.listUser`
to list user private images and :meth:`~dopyapi.images.Image.listApplication` to list application
images available in the market place.

.. _URL: https://cloud.digitalocean.com/account/api/tokens
