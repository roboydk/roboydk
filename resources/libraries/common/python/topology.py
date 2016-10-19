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

"""Defines nodes and topology structure."""

from collections import Counter

from yaml import load

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from resources.libraries.common.python.os_dict import os_napalm_port_map
import pdb

__all__ = ["DICT__nodes", 'Topology']


def _ssh_port_name(node):
    if "linux" in node['os']:
        port = "ssh"
    elif "xr" in node['os']:
        port = "ssh_xr_shell"
    return port


def _convert_list_to_dict(input_list, key_tag):
    _dict_bucket = {}
    key_cnt = 0
    for list_item in input_list:
        key_cnt = key_cnt + 1
        _dict_bucket[key_tag + str(key_cnt)] = list_item

    return _dict_bucket


def _load_topo_from_yaml():
    """Load topology from file defined in "${TOPOLOGY_PATH}" variable.

    :return: Nodes from loaded topology.
    """
    topo_path = BuiltIn().get_variable_value("${TOPOLOGY_PATH}")
    # topo_path = "/Users/mkorshun/IdeaProjects/roboydk_git/resources/topologies/3_node_topology_plus_2_tgens.yml"
    with open(topo_path) as work_file:
        nodes_list = load(work_file.read())['nodes']

        node_cnt = 0
        for node in nodes_list:
            port_dict = _convert_list_to_dict(node["ports"], "port")
            interface_dict = _convert_list_to_dict(node["interfaces"], "interface")
            nodes_list[node_cnt]["ports"] = port_dict
            nodes_list[node_cnt]["interfaces"] = interface_dict
            node_cnt = node_cnt + 1

        return _convert_list_to_dict(nodes_list, "node")


# pylint: disable=invalid-name
class NodeType(object):
    """Defines node types used in topology dictionaries."""
    # Router(This is a router node)
    RTR = 'rtr'
    # Traffic Generator (this node has traffic generator on it)
    TG = 'tgen'
    # Linux (this is a linux node meant for operational tasks)
    LNX = 'lnx'


class NodeSubTypeTG(object):
    """Defines node sub-type TG - traffic generator."""
    # T-Rex traffic generator
    TREX = 'TREX'
    # Moongen
    MOONGEN = 'MOONGEN'
    # IxNetwork
    IXNET = 'IXNET'


DICT__nodes = _load_topo_from_yaml()

print DICT__nodes


class Topology(object):
    """Topology data manipulation and extraction methods.

    Defines methods used for manipulation and extraction of data from
    the active topology.

    "Active topology" contains initially data from the topology file and can be
    extended with additional data from the DUTs like internal interface indexes
    or names. Additional data which can be filled to the active topology are
        - additional internal representation (index, name, ...)
        - operational data (dynamic ports)

    To access the port data it is recommended to use a port key because the key
    does not rely on the data retrieved from nodes, this allows to call most of
    the methods without having filled active topology with internal nodes data.
    """

    @staticmethod
    def get_node_by_name(nodes, name):
        """Get node from nodes of the topology by name.

        :param nodes: Nodes of the test topology.
        :param hostname: User defined name in topo.yml
        :type nodes: dict
        :type name: str
        :return: Node dictionary or None if not found.
        """
        for node in nodes.values():
            if node['name'] == name:
                return node

        return None

    @classmethod
    def get_os_from_node_name(cls, nodes, name):
        """Get node network os from nodes of the topology by name.

        :param nodes: Nodes of the test topology.
        :param hostname: User defined name in topo.yml
        :type nodes: dict
        :type hostname: str
        :return: Node dictionary or None if not found.
        """

        node_ut = cls.get_node_by_name(nodes, name)

        if node_ut is not None:
            return node_ut['os']
        return None

    @classmethod
    def get_mgmtip_from_node_name(cls, nodes, name):
        """Get node Mgmt IP from nodes of the topology by name.

        :param nodes: Nodes of the test topology.
        :param name: User defined name in topo.yml
        :type nodes: dict
        :type hostname: str
        :return: Node dictionary or None if not found.
        """

        node_ut = cls.get_node_by_name(nodes, name)

        if node_ut is not None:
            return node_ut['mgmt_ip']
        return None

    @staticmethod
    def _ssh_port_name(node):
        if "linux" in node['os']:
            port_type = "ssh"
        elif "xr" in node['os']:
            port_type = "ssh_xr"
        return port_type

    @classmethod
    def get_ssh_port_from_node(cls, node):
        """Get ssh port from node. 

        :param node: Node object.
        :return: ssh_port or None if not found.
        """

        ssh_port_name = cls._ssh_port_name(node)
        for port in node["ports"].values():
            if ssh_port_name == port["type"]:
                ssh_port = port["value"]
                return ssh_port

        return None

    @classmethod
    def get_ssh_port_from_node_name(cls, nodes, name):
        """Get ssh port from from nodes of the topology by name. 

        :param nodes: Nodes of the test topology.
        :param hostname: User defined name in topo.yml
        :type nodes: dict
        :type hostname: str
        :return: Node dictionary or None if not found.
        """
        node_ut = cls.get_node_by_name(nodes, name)

        return cls.get_ssh_port_from_node(node_ut)

    @classmethod
    def get_napalm_port_from_node(cls, node):
        """Get ssh port from node. 

        :param node: Node object.
        :return: ssh_port or None if not found.
        """
        napalm_port_name = os_napalm_port_map[node['os']]
        for port in node["ports"].values():
            if napalm_port_name == port["type"]:
                napalm_port = port["value"]
                return napalm_port

        return None

    @classmethod
    def get_napalm_port_from_node_name(cls, nodes, name):
        """Get ssh port from from nodes of the topology by name. 

        :param nodes: Nodes of the test topology.
        :param hostname: User defined name in topo.yml
        :type nodes: dict
        :type hostname: str
        :return: Node dictionary or None if not found.
        """
        node_ut = cls.get_node_by_name(nodes, name)

        return cls.get_napalm_port_from_node(node_ut)

    @staticmethod
    def get_links(nodes):
        """Get list of links(networks) in the topology.

        :param nodes: Nodes of the test topology.
        :type nodes: dict
        :return: Links in the topology.
        :rtype: list
        """
        links = []

        for node in nodes.values():
            for interface in node['interfaces'].values():
                link = interface.get('link')
                if link is not None:
                    if link not in links:
                        links.append(link)

        return links

    @staticmethod
    def _get_interface_by_key_value(node, key, value):
        """Return node interface key from topology file
        according to key and value.

        :param node: The node dictionary.
        :param key: Key by which to select the interface.
        :param value: Value that should be found using the key.
        :type node: dict
        :type key: string
        :type value: string
        :return: Interface key from topology file
        :rtype: string
        """
        interfaces = node['interfaces']
        retval = None
        for if_key, if_val in interfaces.iteritems():
            k_val = if_val.get(key)
            if k_val is not None:
                if k_val == value:
                    retval = if_key
                    break
        return retval

    @classmethod
    def get_interface_by_name(cls, node, iface_name):
        """Return interface key based on name from DUT/TG.

        This method returns interface key based on interface name
        retrieved from the DUT, or TG.

        :param node: The node topology dictionary.
        :param iface_name: Interface name (string form).
        :type node: dict
        :type iface_name: string
        :return: Interface key.
        :rtype: str
        """
        return cls._get_interface_by_key_value(node, "interface", iface_name)

    @classmethod
    def get_interface_by_link_name(node, link_name):
        """Return interface key of link on node.

        This method returns the interface name associated with a given link
        for a given node.

        :param node: The node topology dictionary.
        :param link_name: Name of the link that a interface is connected to.
        :type node: dict
        :type link_name: string
        :return: Interface key of the interface connected to the given link.
        :rtype: str
        """
        return cls._get_interface_by_key_value(node, "link-name", link_name)

    def get_interfaces_by_link_names(self, node, link_names):
        """Return dictionary of dictionaries {"interfaceN", interface name}.

        This method returns the interface names associated with given links
        for a given node.

        :param node: The node topology directory.
        :param link_names: List of names of the link that a interface is
        connected to.
        :type node: dict
        :type link_names: list
        :return: Dictionary of interface names that are connected to the given
        links.
        :rtype: dict
        """
        retval = {}
        interface_key_tpl = "interface{}"
        interface_number = 1
        for link_name in link_names:
            interface = self.get_interface_by_link_name(node, link_name)
            interface_name = self.get_interface_name(node, interface)
            interface_key = interface_key_tpl.format(str(interface_number))
            retval[interface_key] = interface_name
            interface_number += 1
        return retval

    @staticmethod
    def get_adjacent_node_and_interface(nodes_info, node, iface_key):
        """Get node and interface adjacent to specified interface
        on local network.

        :param nodes_info: Dictionary containing information on all nodes
        in topology.
        :param node: Node that contains specified interface.
        :param iface_key: Interface key from topology file.
        :type nodes_info: dict
        :type node: dict
        :type iface_key: str
        :return: Return (node, interface_key) tuple or None if not found.
        :rtype: (dict, str)
        """
        link_name = None
        # get link name where the interface belongs to
        for if_key, if_val in node['interfaces'].iteritems():
            if if_key == 'mgmt':
                continue
            if if_key == iface_key:
                link_name = if_val['link-name']
                break

        if link_name is None:
            return None

        # find link
        for node_data in nodes_info.values():
            # skip self
            if node_data['host'] == node['host']:
                continue
            for if_key, if_val \
                    in node_data['interfaces'].iteritems():
                if 'link-name' not in if_val:
                    continue
                if if_val['link-name'] == link_name:
                    return node_data, if_key

    @staticmethod
    def get_node_interfaces(node):
        """Get all node interfaces.

        :param node: Node to get list of interfaces from.
        :type node: dict
        :return: Return list of keys of all interfaces.
        :rtype: list
        """
        return node['interfaces'].keys()

    @staticmethod
    def _get_node_link_names(node):
        """Return list of link names that are other than mgmt links.

        :param node: Node topology dictionary.
        :param filter_list: Link filter criteria.
        :type node: dict
        :type filter_list: list of strings
        :return: List of strings that represent link names occupied by the node.
        :rtype: list
        """
        interfaces = node['interfaces']
        link_names = []
        for interface in interfaces.values():
            if 'link-name' in interface:
                link_names.append(interface['link'])
        if len(link_names) == 0:
            link_names = None
        return link_names

    @keyword('Get links connecting "${node1}" and "${node2}"')
    def get_connecting_links(self, node1, node2):
        """Return list of link names that connect together node1 and node2.

        :param node1: Node topology dictionary.
        :param node2: Node topology dictionary.
        :param filter_list_node1: Link filter criteria for node1.
        :param filter_list_node2: Link filter criteria for node2.
        :type node1: dict
        :type node2: dict
        :type filter_list_node1: list of strings
        :type filter_list_node2: list of strings
        :return: List of strings that represent connecting link names.
        :rtype: list
        """

        logger.trace("node1: {}".format(str(node1)))
        logger.trace("node2: {}".format(str(node2)))
        node1_links = self._get_node_link_names(node1)
        node2_links = self._get_node_link_names(node2)

        connecting_links = None
        if node1_links is None:
            logger.error("Unable to find links for node1")
        elif node2_links is None:
            logger.error("Unable to find links for node2")
        else:
            connecting_links = list(set(node1_links).intersection(node2_links))

        return connecting_links

    @keyword('Get first active connecting link between node "${node1}" and '
             '"${node2}"')
    def get_first_connecting_link(self, node1, node2):
        """
        :param node1: Connected node.
        :param node2: Connected node.
        :type node1: dict
        :type node2: dict
        :return: Name of link connecting the two nodes together.
        :rtype: str
        :raises: RuntimeError
        """
        connecting_links = self.get_connecting_links(node1, node2)
        if len(connecting_links) == 0:
            raise RuntimeError("No links connecting the nodes were found")
        else:
            return connecting_links[0]

    @keyword('Get egress interfaces name on "${node1}" for link with '
             '"${node2}"')
    def get_egress_interfaces_name_for_nodes(self, node1, node2):
        """Get egress interfaces on node1 for link with node2.

        :param node1: First node, node to get egress interface on.
        :param node2: Second node.
        :type node1: dict
        :type node2: dict
        :return: Egress interfaces.
        :rtype: list
        """
        interfaces = []
        links = self.get_connecting_links(node1, node2)
        if len(links) == 0:
            raise RuntimeError('No link between nodes')
        for interface in node1['interfaces'].values():
            link = interface.get('link-name')
            if link is None:
                continue
            if link in links:
                continue
            name = interface.get('interface')
            if name is None:
                continue
            interfaces.append(name)
        return interfaces

    @keyword('Get first egress interface name on "${node1}" for link with '
             '"${node2}"')
    def get_first_egress_interface_for_nodes(self, node1, node2):
        """Get first egress interface on node1 for link with node2.

        :param node1: First node, node to get egress interface name on.
        :param node2: Second node.
        :type node1: dict
        :type node2: dict
        :return: Egress interface name.
        :rtype: str
        """
        interfaces = self.get_egress_interfaces_name_for_nodes(node1, node2)
        if not interfaces:
            raise RuntimeError('No egress interface for nodes')
        return interfaces[0]

    @staticmethod
    def is_tgen_node(node):
        """Find out whether the node is TG.

        :param node: Node to examine.
        :type node: dict
        :return: True if node is type of TG, otherwise False.
        :rtype: bool
        """
        return node['type'] == NodeType.TG

    @staticmethod
    def get_node_name(node):
        """Return host (hostname/ip address) of the node.

        :param node: Node created from topology.
        :type node: dict
        :return: Hostname or IP address.
        :rtype: str
        """
        return node['name']
