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
| Library | resources.libraries.common.python.netmiko_ssh.NetmikoSSH

*** Test Cases ***

| Exit Config Mode
| | Exit Config Mode
| Enable
| | Enable
| Net Disconnect
| | Net Disconnect | ${node}
| Exit Enable Mode
| | Exit Enable Mode
| Net Connect
| | Net Connect | ${node}
| Find Prompt
| | Find Prompt
| Send Command
| | Send Command | ${cmd}
| Send Config Set
| | Send Config Set | ${config_cmds}
| Check Config Mode
| | Check Config Mode
| Send Config From File
| | Send Config From File | ${cfg_file}
| Clear Buffer
| | Clear Buffer
| Config Mode
| | Config Mode
