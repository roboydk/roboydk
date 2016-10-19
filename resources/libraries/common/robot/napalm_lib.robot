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
| Variables | resources/libraries/common/python/topology.py
| Library | resources.libraries.common.python.napalm_lib.NapalmDriver

*** Test Cases ***
| Compare Config
| | Compare Config
| Get Environment
| | Get Environment
| Get Ntp Stats
| | Get Ntp Stats
| Get Interfaces Counters
| | Get Interfaces Counters
| Get Optics
| | Get Optics |
| Get Bgp Neighbors
| | Get Bgp Neighbors
| Get Snmp Information
| | Get Snmp Information |
| Get Bgp Neighbors Detail
| | Get Bgp Neighbors Detail | ${None}
| Device Setup
| | Device Setup | ${None}
| Get Interfaces Ip
| | Get Interfaces Ip | ${None} ${None}
| Load Merge Candidate
| | Load Merge Candidate | ${None} ${None}
| Get Lldp Neighbors
| | Get Lldp Neighbors
| Open Napalm Session
| | Open Napalm Session | ${None}
| Ping
| | Ping | ${None} ${None} ${None} ${None} ${None} ${None}
| Get Lldp Neighbors Detail
| | Get Lldp Neighbors Detail | ${None}
| Rollback
| | Rollback
| Traceroute
| | Traceroute | ${None} ${None} ${None} ${None}
| Get Interfaces
| | Get Interfaces | ${None} ${None}
| Get Users
| | Get Users |
| Commit Config
| | Commit Config
| Get Bgp Config
| | Get Bgp Config | ${None} ${None}
| Get Mac Address Table
| | Get Mac Address Table |
| Get Route To
| | Get Route To | ${None} ${None}
| Get Config
| | Get Config | ${None}
| Close Napalm Session
| | Close Napalm Session | ${None}
| Get Ntp Servers
| | Get Ntp Servers
| Cli
| | Cli | ${None}
| Load Replace Candidate
| | Load Replace Candidate | ${None} ${None}
| Get Arp Table
| | Get Arp Table
| Get Facts
| | Get Facts
| Discard Config
| | Discard Config



