from ceilometerclient import client as ceilometerclient
from cinderclient import client as cinderclient
from glanceclient import client as glanceclient
from heatclient import client as heatclient
from keystoneclient import client as keystoneclient
from neutronclient.neutron import client as neutronclient
from novaclient import client as novaclient
from swiftclient import client as swiftclient


DEFAULT_SERVICE_VERSIONS = {
    'compute': "2",
    'identity': "3",
    'image': "2",
    'metering': "2",
    'network': "2",
    'orchestration': "1",
    'volume': "2",
}


# a wrapper to facilitate ease of use and avoid the inconsistency
# compared to other client constructors.
def swift_constructor(session, region_name):
    return swiftclient.Connection(
        os_options={'region_name': region_name},
        session=session)


CLIENT_CONSTRUCTORS = {
    'compute': novaclient.Client,
    'identity': keystoneclient.Client,
    'image': glanceclient.Client,
    'metering': ceilometerclient.Client,
    'network': neutronclient.Client,
    'object-store': swift_constructor,
    'orchestration': heatclient.Client,
    'volume': cinderclient.Client,
}


class ServiceNotFound(Exception):
    pass


class ClientManager(object):
    """
    This class is a factory for the various per projects OpenStack clients.
    It is a simple wrapper around all the various constructors in an
    attempt to present them all to you in an easy way by hiding all the
    normal setup, and in some case constructor differences.

    To get a list of what services the ClientManager has been setup for:
    In [1]: oi.clients.available_services

    Default versions for services:
    In [2]: oi.clients.available_services

    To get a client (replace <service_type> with the service you want):
    In [3]: oi.clients.<service_type>

    Get novaclient in your configured region:
    In [4]: novaclient = oi.clients.compute

    Get novaclient in a specific region:
    In [5]: novaclient = oi.clients.get_client(
                'compute', region="RegionOne")

    The python clients themselves have reasonably useful docstrings,
    although the structure and fields of them may be a little unintuitive
    at first. Using the autocomplete functionality of ipython as well as
    <objects>? and <objects>?? should get you most of the way.

    For additional help with the clients look at the offical OpenStack
    client docs (although they are often incomplete or lacking). The
    alternative and often more useful approach is looking at the code
    itself on github.
    """

    def __init__(self, session, default_region):
        self._session = session
        self._default_region = default_region

    def get_client(self, service, version=None, region=None):
        """
        Get an OpenStack client, in a given version, in a given region.

        examples:
        In [1]: novaclient = oi.clients.get_client('compute')
        In [2]: novaclient = oi.clients.get_client(
                    'compute', region="RegionOne")
        In [3]: novaclient = oi.clients.get_client(
                    'compute', version="1")
        """
        try:
            return CLIENT_CONSTRUCTORS[service](
                version or DEFAULT_SERVICE_VERSIONS[service],
                region_name=region or self._default_region,
                session=self._session)
        except KeyError:
            raise ServiceNotFound(service)

    @property
    def available_services(self):
        """
        List available services.
        """
        return CLIENT_CONSTRUCTORS.keys()

    @property
    def default_service_version(self):
        """
        List default service versions.
        """
        return dict(DEFAULT_SERVICE_VERSIONS)

    @property
    def compute(self):
        return self.get_client('compute')

    @property
    def identity(self):
        return self.get_client('identity')

    @property
    def image(self):
        return self.get_client('image')

    @property
    def metering(self):
        return self.get_client('metering')

    @property
    def network(self):
        return self.get_client('network')

    @property
    def object_store(self):
        return self.get_client('object-store')

    @property
    def orchestration(self):
        return self.get_client('orchestration')

    @property
    def volume(self):
        return self.get_client('volume')
