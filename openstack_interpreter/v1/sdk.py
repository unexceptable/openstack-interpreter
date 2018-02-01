from openstack import connection


class SDKManager(object):
    """A wrapper around the openstackSDK

    Your primary interaction will be with the connection itself and
    the various services it exposes. A connection is an authenticated
    object representing a connection to a given cloud region.

    Example get servers:
    In [1]: servers = list(oi.sdk.connection.compute.servers())

    All list methods in the SDK return a generator, so if you don't
    want to act on them in a for loop, you need to explictly ask
    for a list().

    Your best bet to understand what is possible with the connection
    object is to use tab autocomplete and inspect the docstrings of
    the functions themselves.

    fields:
      - connection
          An instance of the openstacksdk connection object built
          from the same session as the openstack interpreter was
          setup via the openstackclient.

    methods:
      - get_connection
          Get a connection object with user defined config.
          For help do:
          In [1]: oi.sdk.get_connection?
    """

    def __init__(self, session):
        self.connection = connection.Connection(session=session)
        self._session = session

    def get_connection(self, **kwargs):
        """Get a connection object with user defined config

        This is mostly used to get a connection to a specific region
        or with specific versions of services.

        All config values will otherwise default to your current
        interpreter session unless overridden. The function takes
        arbitrary kwargs and passes those to the config class.

        The majority of the parameters that will be useful to you
        here are:
            - region_name
            - <service_type>_api_version

        examples:
        In [1]: conn_r2 = oi.sdk.get_connection(region='RegionTwo')
        In [2]: conn_c1 = oi.sdk.get_connection(
                    compute_api_version='2')
        """
        return connection.Connection(session=self._session, **kwargs)
