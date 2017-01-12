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

*** Settings ***
| Library | resources.libraries.common.python.topology.Topology
| Resource | resources/libraries/common/robot/default.robot
#| Resource | resources/libraries/common/robot/topology.robot
#| Resource | resources/libraries/common/robot/openconfig_bgp.robot
| Library | resources.libraries.common.python.ydk.models.openconfig.BGP

#| Test Setup | Setup All DUTs | ${nodes}

*** Variables ***
${NODE1}  rtr1	
${NODE2}  rtr2	

*** Test Cases ***
| TC01: Configure IPv4 BGP instance on rtr1 and rtr3
| | ${node}= | Get node by name | ${nodes} |  ${NODE1} 
| | Config Ipv4 Ibgp | ${node} | Loopback0 | 2.2.2.2 | 65001
| | ${node}= | Get node by name | ${nodes} |  ${NODE2}  
| | Config Ipv4 Ibgp | ${node} | Loopback0 | 1.1.1.1 | 65001
