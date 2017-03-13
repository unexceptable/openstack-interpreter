A simple command to drop you into the python interpreter with the openstack
clients setup.

Using the interpreter
=====================

First install the tool:

::

    pip install openstack-interpreter

The simply run the command. Provided you have your environment variables setup
correctly it will authenticate you, and drop into a python interpreter.

::

    $ os-interpreter

    >>> interpreter
    <openstack_interpreter.OpenStackInterpreter object at 0x7fe39f22b090>
    >>> keystone = interpreter.get_client('identity')
    >>> projects = keystone.projects.list()
    >>> keystone.projects.get(projects[0].id)
    >>> nova = interpreter.get_client('compute')
    >>> servers = nova.servers.list()
    >>> server = nova.servers.get(servers[0].id)
