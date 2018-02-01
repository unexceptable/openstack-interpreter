from IPython import embed

from osc_lib.command import command

from openstack_interpreter.common import output
from openstack_interpreter.common import prompt  # noqa
from openstack_interpreter.common.profile import timed  # noqa
from openstack_interpreter.v1.interpreter import OpenStackInterpreter


def _format_example(line_num, command):
    return (
        output.style_text('In [', ['green']) +
        output.style_text(line_num, ['green-bright', 'bold']) +
        output.style_text(']:', ['green']) +
        command
    )


welcome_msg = """
%(title)s

This is a command added to the OpenStackClient that gives you
quick and easy access to a ipython interpreter that has some
pre-built classes and tools for python development on OpenStack
which are built on top of your authenticated session.

To get started you will probably want to inspect the '%(oi_object)s' object:
%(example_1)s

Most of the objects exposed by the OpenStackInterpreter have useful docstrings
as do some of the underlying libraries and tools such as the OpenStackSDK.

Other useful tools provided along with the OpenStackInterpreter that are
worth inspecting:
%(example_2)s
%(example_3)s
%(example_4)s

And don't forget: %(tab_complete)s

""" % {
    'title': output.style_text(
        "Welcome to the OpenStackInterpreter.", ['bold']),
    'oi_object': output.style_text('oi', ['green']),
    'example_1': _format_example(1, " oi?"),
    'example_2': _format_example(2, " output?"),
    'example_3': _format_example(3, " timed?"),
    'example_4': _format_example(4, " prompt?"),
    'tab_complete': output.style_text(
        "The ipython interpreter supports tab completion!", ['bold']),
}


class SetupOpenStackInterpreter(command.Command):
    """
    Command to setup the interpreter object and drop you into an
    ipython interpreter. You will be authenticated using
    your specificed auth credentials, and the interpreter will be
    setup with your session.

    Your starting interaction will be with the 'oi' object.
    You should also use the help and functionality provided by ipython.

    To get some basic help:
    In [1]: oi?

    Most objects or functions have help and docstrings built in. As such
    using ipython's built in <object>? and <object>?? to see help is useful.
    """

    def _check_auth_url(self):
        auth_url = self.app.client_manager.session.auth.auth_url
        if "v3" in auth_url:
            print(
                output.style_text("WARNING: ", ['yellow', 'bold']) +
                output.style_text(
                    "You are using a versioned Keystone URL.\n"
                    "It is recommended to set OS_AUTH_URL to be versionless,\n"
                    "and control the identity version with: "
                    "OS_IDENTITY_API_VERSION\n"
                    "If you don't, attempting to use the keystoneclient may "
                    "throw errors.",
                    ['yellow']
                )
            )
        if "v2" in auth_url:
            print(
                output.style_text("WARNING: ", ['yellow', 'bold']) +
                output.style_text(
                    "You are using a deprecated Keystone version.\n"
                    "It is highly recommended that you switch to using v3\n"
                    "for your authentication.\n"
                    "It is also recommended to set OS_AUTH_URL to be "
                    "versionless\n"
                    "and control the identity version with: "
                    "OS_IDENTITY_API_VERSION\n"
                    "If you don't, attempting to use the keystoneclient may "
                    "throw errors.",
                    ['yellow']
                )
            )

    def take_action(self, parsed_args):
        self._check_auth_url()
        interpreter = OpenStackInterpreter(self) # noqa
        oi = interpreter # noqa
        print(welcome_msg)
        embed()
