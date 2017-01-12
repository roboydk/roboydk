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

"""Library for YDK provider capabilities."""

from time import time, sleep
import os
from ydk.providers import NetconfServiceProvider
from robot.api import logger
from robot.utils.asserts import assert_equal
from resources.libraries.common.python.topology import Topology
import pdb

class YDKNetconfProvider(object):
    """Contains methods for managing and using YDK provider connections to network devices"""

    __existing_connections = {}

    def __init__(self, proto='ssh'):
        self._session = None
        self._node = None
        self._proto= proto 

    def _node_hash(self, node, port):
        """Get IP address and port hash from node dictionary.

        :param node: Node in topology.
        :param port: 
        :type node: dict
        :return: IP address and port for the specified node.
        :rtype: int
        """

        return hash(frozenset([node['mgmt_ip'], port]))

    def open_netconf_session(self, node):
        """Connect to node using YDK's Netconf service provider.

        """
        self._node = node
        netconf_port = Topology.get_netconf_port_from_node(node)
        print "netconf port Is !!!"+str(netconf_port)
        node_hash = self._node_hash(node, netconf_port)

        if node_hash in YDKNetconfProvider.__existing_connections:
            self._session = YDKNetconfProvider.__existing_connections[node_hash]
            logger.debug('reusing netconf session: {0}'.format(self._session))
        else:
            start = time()
            self._session =  NetconfServiceProvider(address=node['mgmt_ip'],
                                                    port=netconf_port,
                                                    username=node['username'],
                                                    password=node['password'],
                                                    protocol=self._proto)


            YDKNetconfProvider.__existing_connections[node_hash] = self._session

            logger.trace('connect took {} seconds'.format(time() - start))
            logger.debug('new connection: {0}'.format(self._session))


        logger.debug('Connections: {0}'.format(str(YDKNetconfProvider.__existing_connections)))
        return self._session

    def close_netconf_session(self, node):
        """Close netconf connection to the node.

        :param node: The node to disconnect from.
        :type node: dict
        """
        node_hash = self._node_hash(node, netconf)
        if node_hash in YDKNetconfProvider.__existing_connections:
            logger.debug('Disconnecting peer: {}, {}'.
                         format(node['name'], node['port']))
            ssh = YDKNetconfProvider.__existing_connections.pop(node_hash)

        self._session.close()    

    def _reconnect(self):
        """Close the SSH connection and open it again."""

        node = self._node
        self.close_netconf_session(node)
        self.start_netconf_session(node)

