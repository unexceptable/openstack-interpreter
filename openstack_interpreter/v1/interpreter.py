

from openstack_interpreter.v1.clients import ClientManager


class OpenStackInterpreter(object):
    """
    A class to facilitate easy access to the openstack
    python clients and SDKs.

    Additional client help is found at:
    In [1]: interpreter.clients?

    fields:
      - session
          Your keystoneauth session object to reuse as needed.
      - clients
          The interpreter ClientManager. A useful construct to help
          you access all the various python clients.

    """

    def __init__(self, session, default_region):
        self.session = session
        self.clients = ClientManager(
            session=session, default_region=default_region,
        )
