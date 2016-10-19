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
from ydk.services import CRUDService
from robot.api import logger
from robot.utils.asserts import assert_equal
from ydk.models.openconfig import bgp as oc_bgp
from resources.libraries.common.python.ydk.services.crud_service import YDKCrudService


class BGP(object):
    def __init__(self):
        self._crud = YDKCrudService()

    def config_ipv4_ibgp(self, node, loopback, neighbor, as_):
        bgp = oc_bgp.Bgp()
        """Add config data to bgp object."""
        # global configuration
        bgp.global_.config.as_ = as_ 
        v4_afi_safi = bgp.global_.afi_safis.AfiSafi()
        v4_afi_safi.afi_safi_name = "ipv4-unicast"
        v4_afi_safi.config.afi_safi_name = "ipv4-unicast"
        v4_afi_safi.config.enabled = True
        bgp.global_.afi_safis.afi_safi.append(v4_afi_safi)

        # configure IBGP peer group
        ibgp_pg = bgp.peer_groups.PeerGroup()
        ibgp_pg.peer_group_name = "IBGP"
        ibgp_pg.config.peer_group_name = "IBGP"
        ibgp_pg.config.peer_as = as_ 
        ibgp_pg.transport.config.local_address = loopback 
        v4_afi_safi = ibgp_pg.afi_safis.AfiSafi()
        v4_afi_safi.afi_safi_name = "ipv4-unicast"
        v4_afi_safi.config.afi_safi_name = "ipv4-unicast"
        v4_afi_safi.config.enabled = True
        ibgp_pg.afi_safis.afi_safi.append(v4_afi_safi)
        bgp.peer_groups.peer_group.append(ibgp_pg)

        # configure IBGP neighbor
        ibgp_nbr = bgp.neighbors.Neighbor()
        ibgp_nbr.neighbor_address = neighbor 
        ibgp_nbr.config.neighbor_address = neighbor 
        ibgp_nbr.config.peer_group = "IBGP"
        bgp.neighbors.neighbor.append(ibgp_nbr)

        self._crud.create(bgp, node)



DICT__nodes={'node1': {'box': 'ubuntu/trusty64', 'username': 'vagrant', 'name': 'devbox_s', 'mgmt_ip': '10.30.110.213', 'os': 'linux_ubuntu', 'interfaces': {'interface1': {'interface': 'eth1', 'link-name': 'link1'}}, 'password': 'vagrant', 'type': 'tgen', 'ports': {'port1': {'type': 'ssh', 'value': 2522}}}, 'node3': {'box': 'IOS-XRv', 'username': 'vagrant', 'name': 'rtr1', 'mgmt_ip': '10.30.110.213', 'os': 'cisco_iosxr', 'interfaces': {'interface1': {'interface': 'GigabitEthernet0/0/0/0', 'link-name': 'link1'}, 'interface3': {'interface': 'GigabitEthernet0/0/0/2', 'link-name': 'link5'}, 'interface2': {'interface': 'GigabitEthernet0/0/0/1', 'link-name': 'link3'}}, 'password': 'vagrant', 'type': 'rtr', 'ports': {'port2': {'type': 'ssh_xr_shell', 'value': 2602}, 'port3': {'type': 'netconf', 'value': 8301}, 'port1': {'type': 'ssh_xr', 'value': 2601}}}, 'node2': {'box': 'ubuntu/trusty64', 'username': 'vagrant', 'name': 'devbox_r', 'mgmt_ip': 'localhost', 'os': 'linux_ubuntu', 'interfaces': {'interface1': {'interface': 'eth1', 'link-name': 'link2'}}, 'password': 'vagrant', 'type': 'tgen', 'ports': {'port1': {'type': 'ssh', 'value': 2523}}}, 'node5': {'box': 'IOS-XRv', 'username': 'vagrant', 'name': 'rtr3', 'mgmt_ip': 'localhost', 'os': 'cisco_iosxr', 'interfaces': {'interface1': {'interface': 'GigabitEthernet0/0/0/0', 'link-name': 'link4'}, 'interface2': {'interface': 'GigabitEthernet0/0/0/1', 'link-name': 'link5'}}, 'password': 'vagrant', 'type': 'rtr', 'ports': {'port2': {'type': 'ssh_xr_shell', 'value': 2606}, 'port3': {'type': 'netconf', 'value': 8303}, 'port1': {'type': 'ssh_xr', 'value': 2605}}}, 'node4': {'box': 'IOS-XRv', 'username': 'vagrant', 'name': 'rtr2', 'mgmt_ip': 'localhost', 'os': 'cisco_iosxr', 'interfaces': {'interface1': {'interface': 'GigabitEthernet0/0/0/0', 'link-name': 'link3'}, 'interface3': {'interface': 'GigabitEthernet0/0/0/2', 'link-name': 'link4'}, 'interface2': {'interface': 'GigabitEthernet0/0/0/1', 'link-name': 'link2'}}, 'password': 'vagrant', 'type': 'rtr', 'ports': {'port2': {'type': 'ssh_xr_shell', 'value': 2604}, 'port3': {'type': 'netconf', 'value': 8302}, 'port1': {'type': 'ssh_xr', 'value': 2603}}}}


node = DICT__nodes['node3']

BGP().config_ipv4_ibgp(node, "Loopback0", "2.2.2.2", 65001)
