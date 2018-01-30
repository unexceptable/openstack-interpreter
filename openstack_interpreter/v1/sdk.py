from openstack import config as occ
from openstack import connection


class SDKManager(object):
    """
    """

    def __init__(self, config):
        self.connection = connection.from_config(cloud_config=config)
        self._config = config

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
        In [1]: conn_r2 = interpreter.sdk.get_connection(region='RegionTwo')
        In [2]: conn_c1 = interpreter.sdk.get_connection(
                    compute_api_version='2')
        """
        config_values = dict(self._config.config)
        config_values.update(kwargs)

        config = occ.OpenStackConfig(
            load_yaml_config=False, envvar_prefix='GARBAGE'
        ).get_one_cloud(**config_values)

        return connection.from_config(cloud_config=config)
