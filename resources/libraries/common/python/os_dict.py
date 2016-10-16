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

os_netmiko_map = {'cisco_ios': 'cisco_ios',
                  'cisco_iosxe': 'cisco_xe', 
                  'cisco_nxos': 'cisco_nxos', 
                  'cisco_iosxr': 'cisco_xr',
                  'arista_eos': 'arista_eos',
                  'junos': 'juniper',
                  'linux_ubuntu': 'linux',
                  'linux_centos': 'linux'}

os_napalm_map =  {'cisco_ios': 'ios',
                  'cisco_nxos': 'nxos',
                  'cisco_iosxr': 'iosxr',
                  'arista_eos': 'eos',
                  'junos': 'junos',
                  'linux_ubuntu': 'linux',
                  'linux_centos': 'linux'}

os_napalm_port_map = {'cisco_ios': 'ssh',
                      'cisco_nxos': 'nxapi_port',
                      'cisco_iosxr': 'ssh_xr',
                      'arista_eos': 'eapi_port',
                      'junos': 'ssh',
                      'linux_ubuntu': 'ssh',
                      'linux_centos': 'ssh'}
