OpenStack Interpreter
=====================

This is a simple tool to facilitate better python interpreter use of the
various OpenStack python clients and help promote better literacy for
all those tools. The hope is that this tool allows developers to more easily
use and test the various libraries, and also to offer operators a useful tool
for one off operations where writing a script is not needed and where the
OpenStackClient is not flexible enough without resorting to complex bash.


Using the OpenStack Interpreter
-------------------------------

First install the plugin:

::

    pip install openstack-interpreter

This will now be installed as a plugin on the OpenStackClient or install the
OpenStackClient as well.

You will need to either have some environment variables setup, or a
`clouds.yaml` file so that the client can authenticate and setup your
session.

To run the interpreter:

::

    $ openstack interpreter

This will drop you into an ipython interpreter. You will be setup with a
session based on your auth credentials.

Because this is using ipython as the interpreter you can make use of the
autocomplete and help functionality. There is also history search support
and many other features. For more details look at the ipython docs.

To get some basic help you can start with:

::

    In [1]: interpreter?

Or if you want to get and start using the clients, this is how you can get
acess to novaclient:

::

    In [2]: novaclient = interpreter.clients.compute

Or if you want novaclient in a region other than your configured one:

::

    In [2]: novaclient = interpreter.clients.get_client(
                'compute', region='RegionOne')


Development
-----------

Going forward the plan is to add support for OpenStackSDK, and Shade (if I can
find a way to connect it and reuse parts of the same session).

In addition I also want to add more help functionality as is possible.

Adding support for new clients is easy. If you have a client you want added,
make a pull request, or open an issue.

I may be moving this project to OpenStack's gerrit, but in part I'd prefer not
to as the interface for gerrit is awful.
