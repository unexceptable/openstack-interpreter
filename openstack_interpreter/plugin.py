# Copyright 2014 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from osc_lib import utils

LOG = logging.getLogger(__name__)

DEFAULT_OS_INTERPRETER_VERSION = '1'
API_VERSION_OPTION = 'os_interpreter_version'
API_NAME = "interpreter"


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-interpreter-version',
        metavar='<interpreter-version>',
        default=utils.env(
            'OS_INTERPRETER_VERSION',
            default=DEFAULT_OS_INTERPRETER_VERSION),
        help=('Client version, default=' +
              DEFAULT_OS_INTERPRETER_VERSION +
              ' (Env: OS_INTERPRETER_VERSION)'))
    return parser
