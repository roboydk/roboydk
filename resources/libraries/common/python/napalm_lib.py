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

"""Library for SSH connection management. """

from time import time, sleep
from napalm import get_network_driver
from robot.api import logger
from robot.utils.asserts import assert_equal
from resources.libraries.common.python.topology import Topology
from resources.libraries.common.python.os_dict import os_napalm_map, os_napalm_port_map

__all__ = ["exec_cmd", "exec_cmd_no_error"]


class NapalmDriver(object):
    """Contains methods for managing and using SSH connections for Network Devices using Netmiko. Please, make sure,
     that you open napalm session before proceeding with operations on device."""

    __MAX_RECV_BUF = 10 * 1024 * 1024
    __existing_connections = {}

    def __init__(self):
        self._device = None
        self._node = None
        self._napalm_port = None
        self._session = False

    @staticmethod
    def _node_hash(node, port):
        """Get IP address and port hash from node dictionary.

        :param node: Node in topology.
        :param port: 
        :type node: dict
        :return: IP address and port for the specified node.
        :rtype: int
        """

        return hash(frozenset([node['mgmt_ip'], port]))

    @staticmethod
    def _get_driver_type(node):
        device_os = node['os']
        return os_napalm_map[str(device_os)]

    def device_setup(self, node):
        """ Set up Napalm Device Driver based on the Device OS
        :param node: Node in topology.

        """
        self._node = node
        print "NODE is !!!!\n\n"
        print node
        self._napalm_port = Topology.get_napalm_port_from_node(node)

        node_hash = NapalmDriver._node_hash(node, self._napalm_port)
        if node_hash in NapalmDriver.__existing_connections:
            self._device = NapalmDriver.__existing_connections[node_hash]
            logger.debug('reusing ssh: {0}'.format(self._session))
        else:
            start = time()

            driver = get_network_driver(NapalmDriver._get_driver_type(node))

            self._device = driver(hostname=node['mgmt_ip'],
                                  username=node['username'],
                                  password=node['password'],
                                  optional_args={'port': self._napalm_port})

            NapalmDriver.__existing_connections[node_hash] = self._device

            logger.trace('connect took {} seconds'.format(time() - start))
            logger.debug('new device: {0}'.format(self._device))

        logger.debug('Connections: {0}'.format(str(NapalmDriver.__existing_connections)))

    def open_napalm_session(self, node):
        """Open SSH connection to the node.

        :param node: The node to disconnect from.
        :type node: dict
        """
        self.device_setup(node)
        if not self._session:
            self._device.open()
        self._session = True

    def close_napalm_session(self, node):
        """Close SSH connection to the node.

        :param node: The node to disconnect from.
        :type node: dict
        """
   
        node_hash = NapalmDriver._node_hash(node, self._napalm_port)
        if node_hash in NapalmDriver.__existing_connections:
            logger.debug('Removing peer: {}, {}'.
                         format(node['name'], self._napalm_port))
            ssh = NapalmDriver.__existing_connections.pop(node_hash)

        if self._session:
            self._device.close()
        self._session = False

    def _reconnect(self):
        """Close the SSH connection and open it again."""

        node = self._node
        self.close_napalm_session(node)
        self.open_napalm_session(node)

    def load_replace_candidate(self, filename=None, config=None):
        """Napalm function: Load replace candidate.
        :param filename: Node in topology.
        :param config:
        :type config: str
        :type config: str
        """
        node = self._node
        self.open_napalm_session(node)
        self._device.load_replace_candidate(filename, config)

    def load_merge_candidate(self, filename=None, config=None):
        """Napalm function: Load merge candidate.
        :param filename: Node in topology.
        :param config:
        :type config: str
        :type config: str
        """
        node = self._node
        self.open_napalm_session(node)
        self._device.load_merge_candidate(filename, config)

    def compare_config(self):
        """Diff for config"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.compare_config()

    def commit_config(self):
        """Commit for config"""
        node = self._node
        self.open_napalm_session(node)
        self._device.commit_config()

    def discard_config(self):
        """Discard for config"""
        node = self._node
        self.open_napalm_session(node)
        self._device.discard_config()

    def rollback(self):
        """Diff for config"""
        node = self._node
        self.open_napalm_session(node)
        self._device.rollback()

    def get_facts(self):
        """Get facts about device"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_facts()

    def get_interfaces(self):
        """Get device interfaces"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_interfaces()

    def get_lldp_neighbors(self):
        """Get lldp neighbors"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_lldp_neighbors()

    def get_interfaces_counters(self):
        """Get interfaces counters"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_interfaces_counters()

    def get_environment(self):
        """Get environment"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_environment()

    def get_bgp_neighbors(self):
        """Get bgp neighbors"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_bgp_neighbors()

    def get_lldp_neighbors_detail(self, interface=''):
        """Get lldp neighbors on specific port
        :param interface: interface, which you are checking
        :type interface: str
        """
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_lldp_neighbors_detail(interface)

    def cli(self, commands=None):
        """Issue CLI commands
        :param commands:
        :type commands: str
        """
        node = self._node
        self.open_napalm_session(node)
        return self._device.cli(commands)

    def get_bgp_config(self, group='', neighbor=''):
        """Get device BGP commands
        :param group:
        :type neighbor: str
        :param neighbor:
        :type neighbor: str
        """
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_bgp_config(group, neighbor)

    def get_arp_table(self):
        """Get arp table"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_arp_table()

    def get_ntp_servers(self):
        """Get ntp servers"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_ntp_servers()

    def get_ntp_stats(self):
        """Get ntp stats"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_ntp_stats()

    def get_interfaces_ip(self):
        """Get interfaces ip"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_interfaces_ip()

    def get_mac_address_table(self):
        """Get mac address table"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_mac_address_table()

    def get_route_to(self, destination='', protocol=''):
        """Get device BGP commands
        :param destination:
        :type destination: str
        :param protocol:
        :type protocol: str
        """
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_route_to(destination, protocol)

    def get_snmp_information(self):
        """Get device snmp information"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_snmp_information()

    def get_users(self):
        """Get users on device"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_users()

    def traceroute(self, destination, source='', ttl=0, timeout=0):
        """Get device BGP commands
        :param destination:
        :type destination: str
        :param source:
        :type source: str
        :param ttl
        :type ttl: int
        :param timeout: int
        """
        node = self._node
        self.open_napalm_session(node)
        return self._device.traceroute(destination, source, ttl, timeout)

    def get_bgp_neighbors_detail(self, neighbor_address=''):
        """Get bgp neigbors detail
        :param neighbor_address
        :type neighbor_address:str
        """
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_bgp_neighbors_detail(neighbor_address)

    def get_optics(self):
        """ Get device optics"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_optics()

    def get_config(self, retrieve="all"):
        """Get device config"""
        node = self._node
        self.open_napalm_session(node)
        return self._device.get_config(retrieve)

    def ping(self, destination, source='', ttl=255, timeout=2, size=100, count=5):
        """Use ping
        :param destination:
        :type destination: str
        :param source
        :type source: str
        :param ttl
        :type ttl: int
        :param timeout
        :type timeout: int
        :param size
        :type size: int
        :param count
        :type count: int
        """
        node = self._node
        self.open_napalm_session(node)
        return self._device.ping(destination, source, ttl, timeout, size, count)
