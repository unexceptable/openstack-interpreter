#! /usr/bin/env python
import argparse
import code
import os

from keystoneauth1.identity import generic
from keystoneauth1 import session as ksession

from ceilometerclient import client as ceilometerclient
from cinderclient import client as cinderclient
from glanceclient import client as glanceclient
from heatclient import client as heatclient
from keystoneclient import client as keystoneclient
from neutronclient.neutron import client as neutronclient
from novaclient import client as novaclient
from openstack import connection
from openstack import profile

DEFAULT_COMPUTE_VERSION = "2"
DEFAULT_IDENTITY_VERSION = "3"
DEFAULT_IMAGE_VERSION = "2"
DEFAULT_METERING_VERSION = "2"
DEFAULT_NETWORK_VERSION = "2"
DEFAULT_OBJECT_STORAGE_VERSION = "1"
DEFAULT_ORCHESTRATION_VERSION = "1"
DEFAULT_VOLUME_VERSION = "2"


class ServiceNotFound(Exception):
    pass


class OpenStackInterpreter(object):
    """
    A class to facilitate easy access of the openstack
    python clients in an interpreter session if your
    envvars have been setup.

    Example:
    $ python openstack_interpreter.py
    >>> ks = interpreter.get_client('identity')
    >>> ks.projects.list()[0]
    <Project ... >
    >>>
    """

    def __init__(self):
        parser = self.get_parser()
        self.args = parser.parse_args()
        self.authenticate(self.args)

    def get_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '-k', '--insecure',
            default=False,
            action='store_true',
            help=(
                'Explicitly allow this client to perform '
                '"insecure SSL" (https) requests. The server\'s '
                'certificate will not be verified against any '
                'certificate authorities. This option should '
                'be used with caution.'))

        parser.add_argument(
            '--os-cert',
            help=(
                'Path of certificate file to use in SSL '
                'connection. This file can optionally be '
                'prepended with the private key.'))

        parser.add_argument(
            '--os-key',
            help=(
                'Path of client key to use in SSL '
                'connection. This option is not necessary '
                'if your key is prepended to your cert file.'))

        parser.add_argument(
            '--os-cacert',
            metavar='<ca-certificate-file>',
            dest='os_cacert',
            default=os.environ.get('OS_CACERT'),
            help=(
                'Path of CA TLS certificate(s) used to '
                'verify the remote server\'s certificate. '
                'Without this option glance looks for the '
                'default system CA certificates.'))

        parser.add_argument(
            '--os-username',
            default=os.environ.get('OS_USERNAME'),
            help='Defaults to env[OS_USERNAME]')

        parser.add_argument(
            '--os-password',
            default=os.environ.get('OS_PASSWORD'),
            help='Defaults to env[OS_PASSWORD]')

        parser.add_argument(
            '--os-project-id',
            default=os.environ.get(
                'OS_PROJECT_ID', os.environ.get(
                    'OS_TENANT_ID')),
            help='Defaults to env[OS_PROJECT_ID]')

        parser.add_argument(
            '--os-project-name',
            default=os.environ.get(
                'OS_PROJECT_NAME', os.environ.get(
                    'OS_TENANT_NAME')),
            help='Defaults to env[OS_PROJECT_NAME]')

        parser.add_argument(
            '--os-project-domain-id',
            default=os.environ.get('OS_PROJECT_DOMAIN_ID'),
            help='Defaults to env[OS_PROJECT_DOMAIN_ID]')

        parser.add_argument(
            '--os-project-domain-name',
            default=os.environ.get('OS_PROJECT_DOMAIN_NAME'),
            help='Defaults to env[OS_PROJECT_DOMAIN_NAME]')

        parser.add_argument(
            '--os-user-domain-id',
            default=os.environ.get('OS_USER_DOMAIN_ID'),
            help='Defaults to env[OS_USER_DOMAIN_ID]')

        parser.add_argument(
            '--os-user-domain-name',
            default=os.environ.get('OS_USER_DOMAIN_NAME'),
            help='Defaults to env[OS_USER_DOMAIN_NAME]')

        parser.add_argument(
            '--os-auth-url',
            default=os.environ.get('OS_AUTH_URL'),
            help='Defaults to env[OS_AUTH_URL]')

        parser.add_argument(
            '--os-region-name',
            default=os.environ.get('OS_REGION_NAME'),
            help='Defaults to env[OS_REGION_NAME]')

        parser.add_argument(
            '--os-token',
            default=os.environ.get('OS_TOKEN'),
            help='Defaults to env[OS_TOKEN]')

        return parser

    def authenticate(self, args):
        if args.insecure:
            verify = False
        else:
            verify = args.os_cacert or True
        if args.os_cert and args.os_key:
            cert = (args.os_cert, args.os_key)
        else:
            cert = None

        if args.os_token:
            kwargs = {
                'token': args.os_token,
                'auth_url': args.os_auth_url,
                'username': args.os_username,
                'project_id': args.os_project_id,
                'project_name': args.os_project_name,
                'project_domain_id': args.os_project_domain_id,
                'project_domain_name': args.os_project_domain_name,
            }
            self.auth = generic.Token(**kwargs)
            self.session = ksession.Session(
                auth=self.auth, verify=verify, cert=cert)
        else:
            kwargs = {
                'username': args.os_username,
                'password': args.os_password,
                'auth_url': args.os_auth_url,
                'project_id': args.os_project_id,
                'project_name': args.os_project_name,
                'project_domain_id': args.os_project_domain_id,
                'project_domain_name': args.os_project_domain_name,
                'user_domain_id': args.os_user_domain_id,
                'user_domain_name': args.os_user_domain_name,
            }
            self.auth = generic.Password(**kwargs)
            self.session = ksession.Session(
                auth=self.auth, verify=verify, cert=cert)

    def get_client(self, service, region=None, version=None):
        region = region or self.args.os_region_name

        if service == 'compute':
            return novaclient.Client(
                version or DEFAULT_COMPUTE_VERSION,
                session=self.session, region_name=region)
        if service == 'identity':
            return keystoneclient.Client(
                version or DEFAULT_IDENTITY_VERSION,
                session=self.session, region_name=region)
        if service == 'image':
            return glanceclient.Client(
                version or DEFAULT_IMAGE_VERSION,
                session=self.session, region_name=region)
        if service == 'metering':
            return ceilometerclient.Client(
                version or DEFAULT_METERING_VERSION,
                session=self.session, region_name=region)
        if service == 'network':
            return neutronclient.Client(
                version or DEFAULT_NETWORK_VERSION,
                session=self.session, region_name=region)
        # The swift client is awful, and doesn't support session.
        if service == 'object-store':
            prof = profile.Profile()
            prof.set_region("object-store", region)
            prof.set_version(
                "object-store", version or DEFAULT_OBJECT_STORAGE_VERSION)
            prof.set_interface("object-store", 'public')
            conn = connection.Connection(
                authenticator=self.session.auth,
                verify=self.session.verify,
                cert=self.session.cert,
                profile=prof)
            return conn.object_store
        if service == 'orchestration':
            return heatclient.Client(
                version or DEFAULT_ORCHESTRATION_VERSION,
                session=self.session, region_name=region)
        if service == 'volume':
            return cinderclient.Client(
                version or DEFAULT_VOLUME_VERSION,
                session=self.session, region_name=region)

        raise ServiceNotFound(service)


def setup():
    interpreter = OpenStackInterpreter()
    try:
        interpreter.session.get_token()
        code.interact(local=locals())
    except AttributeError:
        print("ERROR: Environment varibles not setup.")


if __name__ == '__main__':
    setup()
