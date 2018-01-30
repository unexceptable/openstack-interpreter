
from openstack_interpreter.v1.clients import ClientManager
from openstack_interpreter.v1.sdk import SDKManager


class OpenStackInterpreter(object):
    """
    A class to facilitate easy access to the openstack
    python clients and SDKs.

    Additional client help is found at:
    In [1]: oi.sdk?
    In [2]: oi.clients?

    fields:
      - session
          Your keystoneauth session object to reuse as needed.
      - clients
          The interpreter ClientManager. A useful construct to help
          you access all the various python clients.
      - sdk
          The interpreter SDKManager. A wrapper around the openstack sdk
          with some helper functions for setup.

    """

    def __init__(self, command):
        self._session = command.app.client_manager.session
        self.clients = ClientManager(
            session=self._session,
            default_region=command.app.client_manager.region_name,
        )
        self.sdk = SDKManager(session=self._session)
