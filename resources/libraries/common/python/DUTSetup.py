# Copyright (c) 2016 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""DUT setup library."""

from robot.api import logger

from resources.libraries.common.python.topology import NodeType
from resources.libraries.common.python.ssh import SSH


class DUTSetup(object):
    @staticmethod
    def setup_all_duts(nodes):
        """Prepare all DUTs in given topology for test execution."""
        for node in nodes.values():
            DUTSetup.setup_dut(node)

    @staticmethod
    def setup_dut(node):
        """Run script over SSH to setup the DUT node.

        :param node: DUT node to set up.
        :type node: dict

        :raises Exception: If the DUT setup fails.
        """
        ssh = SSH()
        ssh.connect(node)

        (ret_code, stdout, stderr) = \
            ssh.exec_command('ls') 
        logger.trace(stdout)
        logger.trace(stderr)
        if int(ret_code) != 0:
            logger.debug('DUT {0} setup script failed: "{1}"'.
                         format(node['host'], stdout + stderr))
            raise Exception('DUT test setup script failed at node {}'.
                            format(node['host']))
