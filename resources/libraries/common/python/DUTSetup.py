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
from resources.libraries.common.python.netmiko_ssh import NetmikoSSH 
from resources.libraries.common.python.napalm_lib import NapalmDriver
from os.path import expanduser
home = expanduser("~")

class DUTSetup(object):
    @staticmethod
    def setup_all_duts(nodes):
        """Prepare all DUTs in given topology for test execution."""
        for node in nodes.values():
              print "*WARN*"+str(node['name'])
              DUTSetup.setup_dut(node)

    @staticmethod
    def _get_napalm_base_config(node):
    ## TODO: Add the base configs of remaining OS's.

        def iosxr_base_config():
            config_list = ['xml agent ssl',
                           'xml agent tty',
                           'commit']
            return config_list
 
        def eos_base_config():
            config_list = ['management api http-commands',
                            'no shutdown',
                            'exit',
                            'username '+node['username']+' secret '+node['password']]
            return config_list

        def nxos_base_config():
            for port in node["ports"].values():
                if 'nxapi_port' == port["type"]:
                  config_list = ['feature nxapi',
                                 'nxapi http port '+ port['value']]
                else:
                  config_list = [] 
            return config_list

        node_os_dict = {'cisco_nxos': nxos_base_config(),
                        'cisco_iosxr': iosxr_base_config(),
                        'arista_eos': eos_base_config()}

        return node_os_dict[node['os']]

    @staticmethod
    def setup_dut(node):
        """Run script over SSH to setup the DUT node.

        :param node: DUT node to set up.
        :type node: dict

        :raises Exception: If the DUT setup fails.
        """
        net_session = NetmikoSSH() 
        net_session.net_connect(node)

        #output = net_session.send_command("show version") 

        #print "*WARN*"+str(output)

        if node['type'] == NodeType.RTR:
            print DUTSetup._get_napalm_base_config(node)
            output = net_session.send_config_set(DUTSetup._get_napalm_base_config(node))
            print output
            napalm = NapalmDriver()
            napalm.open_napalm_session(node)
            napalm.load_merge_candidate(home+"/configs/"+node["name"]+"_config")
            output = napalm.compare_config()
            print "*WARN*"+str(output)

            napalm.commit_config() 
        


#DICT__nodes={'node1': {'box': 'ubuntu/trusty64', 'username': 'vagrant', 'name': 'devbox_s', 'mgmt_ip': 'localhost', 'os': 'linux_ubuntu', 'interfaces': {'interface1': {'interface': 'eth1', 'link-name': 'link1'}}, 'password': 'vagrant', 'type': 'tgen', 'ports': {'port1': {'type': 'ssh', 'value': 2522}}}, 'node3': {'box': 'IOS-XRv', 'username': 'vagrant', 'name': 'rtr1', 'mgmt_ip': 'localhost', 'os': 'cisco_iosxr', 'interfaces': {'interface1': {'interface': 'GigabitEthernet0/0/0/0', 'link-name': 'link1'}, 'interface3': {'interface': 'GigabitEthernet0/0/0/2', 'link-name': 'link5'}, 'interface2': {'interface': 'GigabitEthernet0/0/0/1', 'link-name': 'link3'}}, 'password': 'vagrant', 'type': 'rtr', 'ports': {'port2': {'type': 'ssh_xr_shell', 'value': 2602}, 'port3': {'type': 'netconf', 'value': 8301}, 'port1': {'type': 'ssh_xr', 'value': 2601}}}, 'node2': {'box': 'ubuntu/trusty64', 'username': 'vagrant', 'name': 'devbox_r', 'mgmt_ip': 'localhost', 'os': 'linux_ubuntu', 'interfaces': {'interface1': {'interface': 'eth1', 'link-name': 'link2'}}, 'password': 'vagrant', 'type': 'tgen', 'ports': {'port1': {'type': 'ssh', 'value': 2523}}}, 'node5': {'box': 'IOS-XRv', 'username': 'vagrant', 'name': 'rtr3', 'mgmt_ip': 'localhost', 'os': 'cisco_iosxr', 'interfaces': {'interface1': {'interface': 'GigabitEthernet0/0/0/0', 'link-name': 'link4'}, 'interface2': {'interface': 'GigabitEthernet0/0/0/1', 'link-name': 'link5'}}, 'password': 'vagrant', 'type': 'rtr', 'ports': {'port2': {'type': 'ssh_xr_shell', 'value': 2606}, 'port3': {'type': 'netconf', 'value': 8303}, 'port1': {'type': 'ssh_xr', 'value': 2605}}}, 'node4': {'box': 'IOS-XRv', 'username': 'vagrant', 'name': 'rtr2', 'mgmt_ip': 'localhost', 'os': 'cisco_iosxr', 'interfaces': {'interface1': {'interface': 'GigabitEthernet0/0/0/0', 'link-name': 'link3'}, 'interface3': {'interface': 'GigabitEthernet0/0/0/2', 'link-name': 'link4'}, 'interface2': {'interface': 'GigabitEthernet0/0/0/1', 'link-name': 'link2'}}, 'password': 'vagrant', 'type': 'rtr', 'ports': {'port2': {'type': 'ssh_xr_shell', 'value': 2604}, 'port3': {'type': 'netconf', 'value': 8302}, 'port1': {'type': 'ssh_xr', 'value': 2603}}}}

#DUTSetup().setup_all_duts(DICT__nodes)
