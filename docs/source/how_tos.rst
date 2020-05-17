=======================
How to use the Library?
=======================

In this section we will describe the structure of the library
needed by the users who want to consume it.

Digital Ocean resources as classes
----------------------------------

Every resource in Digital Ocean is represented by a class here, this
class inherits from :class:`~dopyapi.resource.Resource` class, you
do not need to use the :class:`~dopyapi.resource.Resource` class directly
just use the classes that inherit from it.

The class that represents a resource has a name that is singular, and starts
with a capital letter for the resource, for example: droplets have a class
called :class:`~dopyapi.resource.Droplet`, Firewalls have a class called
:class:`~dopyapi.resource.Firewall` and so on.

Common methods
---------------

Every class that represents a Digital Ocean resource has these common methods

* :meth:`~dopyapi.resource.Resource.list`: This method is used to retrieve instances of the resource based on its
  parameters which include ``page`` and ``per_page`` which default to
  1 and 20 respectively, these define how many instances are returned
  and where to start returning them, for example: ``page = 3`` and ``per_page = 40``
  means return 40 instances starting from page 3 if we had a total of 120
  instances for this resource then we will return the last 40.
* :meth:`~dopyapi.resource.Resource.create`: This method is used to create instances of resources, you pass
  the names of dynamic attributes along with their values as parameters
  and it creates the resource then updates the current object.
* :meth:`~dopyapi.resource.Resource.save`: This method is used to save any changes we do to the dynamic attributes
  of an object, it sends a PUT request along with the values of all dynamic
  attributes to save them all.
* :meth:`~dopyapi.resource.Resource.json`: This method returns a json representation of the resource, that
  is a python dictionary with one key equals to the resource name and
  its value is another dictionary which contains values for all attributes.
* :meth:`~dopyapi.resource.Resource.delete`: The delete method is used to delete an instance of a resource.
* :meth:`~dopyapi.resource.Resource.listActions`: This method is used to list all actions associated with a resource.
* :meth:`~dopyapi.resource.Resource.getAction`: This method is used to fetch the action associated with a resource using its action ID.
* :meth:`~dopyapi.resource.Resource.getID`: This method returns the value for the ID attribute, it could be a string or integer according to the resource.

Fetch single instance of a resource
-----------------------------------

Now we will talk about an important part of our Library, how to fetch
resources based on the value of an attribute?

From Digital Ocean documentation it says that we can for example fetch
a droplet based on its ID, so how to do this here?

If you are thinking about a method such as ``get_by_id`` then you are
wrong, we do not use methods here to do the job, we simply assign a value
to the ID attribute and we have the object ready to get values for any attribute
we want, check this code to understand better::

  import dopyapi as do
  do.authenticate()
  droplets = do.Droplet.list() # We fetched a list of all droplets
  print(droplets[0]) # Here we print the droplet object, which will show its ID
  droplet = do.Droplet() # we declare an object of class Droplet
  droplet.id = droplets[0].id # Here we just assign a value for the ID attribute
  print(droplet.json()) # Here we print a JSON representation of the droplet

You will notice that the ID of the last object ``droplet`` is the same as
the ID of the first object of the list ``droplets`` and also all of its
attribute values are the same too.

Where is the API call? It is actually hidden inside the :class:`~dopyapi.resource.Resource`
this call is only made once when we need it, so we do not bother our selves
with the call.

All other classes use the same technique, each resource has its own attributes
that can be used when fetching for example: Volumes can be fetched by ID, Floating IPs
can be fetched by their IP address, Images can be fetched by their ID or slug. etc...
