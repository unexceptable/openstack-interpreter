from IPython import embed

from osc_lib.command import command

from openstack_interpreter.common import output
from openstack_interpreter.v1.interpreter import OpenStackInterpreter


class SetupOpenStackInterpreter(command.Command):
    """
    Command to setup the interpreter object and drop you into an
    ipython interpreter. You will be authenticated using
    your specificed auth credentials, and the interpreter will be
    setup with your session.

    Your starting interaction will be with the 'interpreter' object.
    You should also use the help and functionality provided by ipython.

    To get some basic help:
    In [1]: interpreter?

    Most objects or functions have help and docstrings built in. As such
    using ipython's built in <object>? and <object>?? to see help is useful.
    """

    def _check_auth_url(self):
        auth_url = self.app.client_manager.session.auth.auth_url
        if "v3" in auth_url:
            output.print_yellow(
                "WARNING: You are using a versioned Keystone URL.\n"
                "It is recommended to set OS_AUTH_URL to be versionless,\n"
                "and control the identity version with: "
                "OS_IDENTITY_API_VERSION\n"
                "If you don't, attempting to use the keystoneclient may "
                "throw errors."
                )
        if "v2" in auth_url:
            output.print_yellow(
                "WARNING: You are using a deprecated Keystone version.\n"
                "It is highly recommended that you switch to using v3\n"
                "for your authentication.\n"
                "It is also recommended to set OS_AUTH_URL to be versionless\n"
                "and control the identity version with: "
                "OS_IDENTITY_API_VERSION\n"
                "If you don't, attempting to use the keystoneclient may "
                "throw errors."
                )

    def take_action(self, parsed_args):
        self._check_auth_url()
        interpreter = OpenStackInterpreter(
            session=self.app.client_manager.session,
            default_region=self.app.client_manager.region_name,
        )
        embed()
