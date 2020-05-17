=============
Magic Methods
=============

.. note::
  This part is intended to describe an internal aspect of the library that is
  only needed by people who want to develop the library itself and not use it
  if you only want to use the library in your own projects then you may skip
  this part however if you have some good python experience and want to know
  the library internally then go ahead and read.

What are python magic methods
-----------------------------

Magic methods are like normal methods in Python but they are not called
directly by programmers, they are called by python interpreter behind
the scenes each one of them at specific time or in a specific situation,
for example we have ``__init__`` magic method that is called when we create
an object of a class, ``__del__`` which is called when we delete an object
of a class or it gets out of scope.

These methods start with ``__`` and end with it too, so when we name methods
we better not use this syntax.

.. note::
  We will not explain all python magic methods here, to learn more
  follow this `link`_.

.. _link: https://rszalski.github.io/magicmethods/

Attribute get and set magic methods
-----------------------------------

There are two magic methods used here the first one is ``__getattribute__``
which is called every time we access an attribute of an object, and
``__setattr__`` that is called every time we set a value for an attribute.

Look at this code::

  class A:
    def __getattribute__(self, attr):
      try:
        return object.__getattribute__(self, attr)
      except AttributeError:
        return "attribute not found"
    def __setattr__(self, attr, value):
      object.__setattr__(self, attr, value)
  a = A()
  a.x = 3
  print(a.x)
  print(a.y)

In the previous code we used these methods to explain their usage.
Every time we try to set a value for an attribute, as found in line 10
``a.x = 3``, the method ``__setattr__`` is called, which calls the
``__setattr__`` method on the object called ``object`` that is
the parent for all objects in python.

And every time we try to access an attribute value, the method ``__getattribute__``
is called and tries to get the value using the ``object`` object, if
it is not available then it returns the string "attribute not found", this
is for demonstration purposes only.

Resource class magic methods
----------------------------

In our library we have the class :class:`~dopyapi.resource.Resource`, that is
the parent for all Digital Ocean resources, most of the magic happens in this
class that was written carefully to help us implement other functionality
easily, this class has these two magic methods :meth:`~dopyapi.resource.Resource.__getattribute__`
and :meth:`~dopyapi.resource.Resource.__setattr__`.

Here is the code for the ``__getattribute__`` method::

  if attr == "resource":
        return object.__getattribute__(self, attr)
    resource = object.__getattribute__(self, "resource")
    static_attrs = resource.static_attrs
    dynamic_attrs = resource.dynamic_attrs
    fetch_attrs = resource.fetch_attrs
    action_attrs = resource.action_attrs
    if attr in static_attrs or attr in dynamic_attrs or attr in fetch_attrs:
        return self.__fetch(attr)
    if attr in action_attrs:
        return lambda **kwargs : self.action(type=attr, **kwargs)
    return object.__getattribute__(self, attr)

From the previous code we can see that the `resource` attribute is treated
first, this attribute holds the class of Digital Ocean resource, if we
are using :class:`~dopyapi.droplets.Droplet` then instance would be
``Droplet``, this class has a list of class attributes that define the
resource, some of them are ``static_attrs``, ``dynamic_attrs``, ``fetch_attrs``
and ``action_attrs``, we will explain them now.

* ``static_attrs``: These attributes are set by Digital Ocean and cannot
  be changed directly.
* ``dynamic_attrs``: These attributes are set by users and can be changed,
  they are used when creating resources or updating them.
* ``fetch_attrs``: These attributes are set by Digital Ocean and can
  be used to fetch resources based on them for example: we can fetch
  a droplet based on its ID.
* ``action_attrs``: These are the defined actions for the resource,
  if a resource does not have any actions associated with it then this
  list will be empty.

If you check the code again, you can see that if the attribute is one of
``fetch_attrs``, ``static_attrs`` or ``dynamic_attrs`` we call ``__fetch``
method, whcih checks if we previously fetched from the API and populated
the object with data, it simply returns the value for the attribute, if not
it calls ``__do_fetch`` that will fetch data from the API.

If the attribute is in ``action_attrs``, it returns a lambda function
that calls the :meth:`~dopyapi.resource.Resource.action` method with the
correct type.

With this method we transparently call API only when needed, but what
if the value of one attribute changes? How can we detect this and refresh
from the API? The answer is in ``__setattr__`` magic method.

Here is the code for the ``__setattr__`` magic method::

  if attr == "resource":
        object.__setattr__(self, attr, value)
    resource = object.__getattribute__(self, "resource")
    static_attrs = resource.static_attrs
    dynamic_attrs = resource.dynamic_attrs
    fetch_attrs = resource.fetch_attrs
    if attr in fetch_attrs:
        self.__dict__["__changed"] = attr
        self.__dict__["__fetched"] = False
    if attr in static_attrs:
        return
    self.__dict__[attr] = value

From the previous code we can see, if the attribute is in ``fetch_attrs``
then we set the value for ``__changed`` to the name of the attribute
and ``__fetched`` to False, with this way if we try to get the value of
an attribute the class can detect the change and call the API to update.

We can also see that if the attribute is in ``static_attrs`` it returns
without updating its value because these attributes are set by Digital Ocean
and cannot be changed directly.

With these two methods we gave our library the ability to call the API
transparently when needed and help users use our classes as they would
do with any other classes.
