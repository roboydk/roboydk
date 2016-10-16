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

"""Library for SSH connection management."""

from time import time, sleep
import os
from netmiko import ConnectHandler
from robot.api import logger
from robot.utils.asserts import assert_equal
from resources.libraries.common.python.topology import Topology
from resources.libraries.common.python.os_netmiko_dict import os_netmiko_map
import pdb

class NetmikoSSH(object):
    """Contains methods for managing and using SSH connections for Network Devices using Netmiko"""

    __MAX_RECV_BUF = 10*1024*1024
    __existing_connections = {}

    def __init__(self):
        self._session = None
        self._node = None
        self._device = {} 

    @staticmethod
    def _node_hash(self, node, port):
        """Get IP address and port hash from node dictionary.

        :param node: Node in topology.
        :param port: 
        :type node: dict
        :return: IP address and port for the specified node.
        :rtype: int
        """

        return hash(frozenset([node['mgmt_ip'], port]))


    @staticmethod
    def _get_device_type(node):
        device_os = node['os'] 
        if str(device_os) in os_netmiko_map.keys():
          return os_netmiko_map[str(device_os)] 
        return None

    def net_connect(self, node):
        """Connect to node using Netmiko's inbuilt libraries.

        """
        self._node = node
        ssh_port = Topology.get_ssh_port_from_node(node)

        node_hash = self._node_hash(self, node, ssh_port)
        if node_hash in NetmikoSSH.__existing_connections:
            self._session = NetmikoSSH.__existing_connections[node_hash]
            logger.debug('reusing ssh: {0}'.format(self._session))
        else:
            start = time()
            self._device = {'device_type': NetmikoSSH._get_device_type(node),
                            'ip': node['mgmt_ip'],
                            'username': node['username'],
                            'password': node['password'],
                            'port': ssh_port }


            self._session = ConnectHandler(**self._device)
            NetmikoSSH.__existing_connections[node_hash] = self._session

            logger.trace('connect took {} seconds'.format(time() - start))
            logger.debug('new connection: {0}'.format(self._session))


        logger.debug('Connections: {0}'.format(str(NetmikoSSH.__existing_connections)))

    def net_disconnect(self, node):
        """Close SSH connection to the node.

        :param node: The node to disconnect from.
        :type node: dict
        """
        node_hash = self._node_hash(node)
        if node_hash in NetmikoSSH.__existing_connections:
            logger.debug('Disconnecting peer: {}, {}'.
                         format(node['host'], node['port']))
            ssh = NetmikoSSH.__existing_connections.pop(node_hash)

        self._session.disconnect()    

    def _reconnect(self):
        """Close the SSH connection and open it again."""

        node = self._node
        self.net_disconnect(node)
        self.net_connect(node)

    def config_mode(self):
        """Enter into config mode """
        self.net_connect(self._node)
        self._session.config_mode()

    def check_config_mode(self):
        """ Check if session is currently in config mode"""
        self.net_connect(self._node)
        return self._session.check_config_mode()

    def exit_config_mode(self):
        """Exit config mode"""
        self.net_connect(self._node)
        self._session.exit_config_mode()

    def clear_buffer(self):
        """ Clear logging buffer """
        self.net_connect(self._node)
        self._session.clear_buffer()

    def enable(self):
        """ Enter Enable Mode"""
        self.net_connect(self._node)
        self._session.enable()

    def exit_enable_mode(self):
        """ Exit enable mode """
        self.net_connect(self._node)
        self._session.exit_enable_mode()

    def find_prompt(self):
        """Return the current router prompt"""
        self.net_connect(self._node)
        self._session.find_prompt()

    def send_command(self, cmd):
        """Send command down the SSH channel and return output back"""
        if cmd is None:
          raise TypeError('Command parameter is None')
        if len(cmd) == 0:
          raise ValueError('Empty command parameter')

        self.net_connect(self._node)
        return self._session.send_command(cmd)

    def send_config_set(self, config_cmds):
        """Send a set of configuration commands to remote device"""
        if config_cmds is None:
          raise TypeError('Config Cmds parameter is None')
        self.net_connect(self._node)
        print "Netmiko NODE !!!\n\n"
        print self._node
        return self._session.send_config_set(config_cmds)

    def send_config_from_file(self, cfg_file):
        """Send a set of configuration commands loaded from a file """
        if not os.path.isfile(cfg_file):
          raise TypeError('Config file does not exist')
        self.net_connect(self._node)
        self._session.send_config_from_file(cfg_file)
