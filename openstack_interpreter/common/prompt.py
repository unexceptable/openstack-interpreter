# Copyright (c) 2016 Catalyst IT Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
This module is focused on adding a prompt to some action where you want to be
able to have something stop, and ask for input before moving on.

It is suggested you use tab autocomplete to list the available functions
in this class, and inspect them for their docstrings.

An example use case:
In [1]: for server in oi.sdk.connection.compute.servers():
...:     if server.status == "ERROR":
...:         if prompt.prompt_yes_no(
...:                 "Do you wish to delete server '%s'" % server.name):
...:             server.delete()
...:     else:
...:         print(server.name)
"""


from random import randint
import sys


def prompt_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def prompt_safe(question):
    """Generate and print a random 4 digit int, user must type same number."""
    safe_check = str(randint(0000, 9999))
    prompt = "\nType the following number to confirm: %s\n> " % safe_check
    sys.stdout.write(question + prompt)
    choice = raw_input().lower()
    if choice == safe_check:
        return True
    else:
        return False
