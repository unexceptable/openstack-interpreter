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

    In [1]: oi?

Or if you want to get and start using the sdk, this is how you can get
access to it:

::

    In [2]: conn = oi.sdk.connection

Or if you want the sdk connection in a region other than your configured or
default one:

::

    In [2]: conn = oi.sdk.get_connection(region_name='RegionOne')


Additional inbuilt tools
------------------------

This library has a few basic tools for helping you deal with the data you are
playing with and present it to you a little nicer. This will improve over time
as more is added, but for now we have some output functions, basic profiling,
and a few prompts.

tools examples
**************

Maybe you want to look at some of the values on an OpenStack resource. Since
most of the client libraries give resources a to_dict function (NOTE: this may
not always be the case) you can do the following:

::

    servers = list(conn.compute.servers())

    output.print_dict(servers[0].to_dict())

Or just print the object itself, since it may not have to_dict anyway:

::

    output.print_object(servers[0])

Although some of the fields may be dicts and this harder to read, so we'd like
to format them a little:

::

    output.print_object(
        servers[0], formatters={
            'addresses': output.json_formatter,
            'flavor': output.json_formatter,
            'image': output.json_formatter,
            'links': output.json_formatter})

Or maybe you're looking at a list of resources, and you only care about certain
fields:

::

    output.print_list(servers, ["name", "id", "status"])

You can even format lists, although be careful as listing does not auto wrap
properly yet:

::

    output.print_list(
        servers, ['name', 'status', 'addresses'],
            formatters={'addresses': output.json_formatter})

Or maybe you are looking at a lot of data and want to highlight something:

::

    rows = []

    for server in servers:
        if server.status == "ACTIVE":
            rows.append([
                server.name, server.id,
                output.style_text(server.status, ['green', 'bold'])
            ])
        elif server.status == "ERROR":
            rows.append([
                server.name, server.id,
                output.style_text(server.status, ['red', 'bold'])
            ])
        else:
            rows.append([server.name, server.id, server.status])

    output.print_list_rows(rows, ["name", "id", "status"])

Or want to delete a ton of instances, but want ones with certain names (or
maybe even tags) to ask for a prompt first:

::

    for server in conn.compute.servers():
        if "prod" in server.name:
            output.print_object(server)
            if prompt.prompt_yes_no(
                    "Are you sure you want to delete this?"):
                server.delete()
        else:
            server.delete()

Or maybe you're just curious how long it takes to run something:

::

    with timed("listing servers"):
        servers = list(conn.compute.servers())

Useful patterns
---------------

Get my servers (or any resource) across all regions:

::

    servers = {}

    for region in conn.identity.regions():
        servers[region.id] = list(oi.sdk.get_connection(
            region_name=region.id).compute.servers())

Development
-----------

I want to add more help functionality as is possible, hopefully even something
that is interactive such as a tutorial.

I may be moving this project to OpenStack's gerrit, but in part I'd prefer not
to as the interface for gerrit is awful, although I may end up moving this to
gitlab, adding some tests and a build via gitlab runners.
