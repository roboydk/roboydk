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
from resources.libraries.common.python.ydk.providers.netconf_provider import YDKNetconfProvider
import pdb

class YDKCrudService(object):
    """Contains methods for sending create/read/update/delete operations over a YDK provider"""

    __existing_connections = {}

    def __init__(self):
        self._session = None
        self._crud = CRUDService()


    def _open_provider_session(self, node, protocol="netconf", provider_proto='default'):

        def netconf():
            """
            Return the YDK netconf provider 
            """
            if provider_proto == 'default':
               netconf_proto = 'ssh'
            else:
               netconf_proto = provider_proto

            provider =  YDKNetconfProvider(netconf_proto)
            self._session = provider.open_netconf_session(node)
            return self._session

        def grpc():
            ##TODO: when grpc gets implemented by YDK as a provider.
            return None


        provider_dict = {'netconf': netconf(),
                         'grpc': grpc()}


        return provider_dict[protocol] 

    def _close_provider_session(self, node):

        def netconf():
            """
            Return the YDK netconf provider 
            """

            provider =  YDKNetconfProvider()
            self._session = provider.close_netconf_session(node)
            return self._session

        def grpc():
            ##TODO: when grpc gets implemented by YDK as a provider.
            return None


        provider_dict = {'netconf': netconf(),
                         'grpc': grpc()}


        return provider_dict[protocol]

    def create(self, entity, node, protocol="netconf", provider_proto='default'):
        """Invoke a crud.create for a given entity on a node using the specified protocol.

        """

        # Open up the provider session if necessary
        self._open_provider_session(node, protocol, provider_proto)        
       
        # Initiate a crud.create on the selected provider

        self._crud.create(self._session, entity)

        logger.debug('Crud Create Successful')
        self._close_provider_session(node)

    def read(self, entity, node, protocol="netconf", provider_proto='default'):
        """Invoke a crud.create for a given entity on a node using the specified protocol.

        """

        # Open up the provider session if necessary
        self._open_provider_session(node, protocol, provider_proto)          

        # Initiate a crud.create on the selected provider

        self._crud.read(self._session, entity)

        logger.debug('Crud Read Successful')


    def update(self, entity, node, protocol="netconf", provider_proto='default'):
        """Invoke a crud.create for a given entity on a node using the specified protocol.

        """

        # Open up the provider session if necessary
        self._open_provider_session(node, protocol, provider_proto)

        # Initiate a crud.create on the selected provider

        self._crud.update(self._session, entity)

        logger.debug('Crud Update Successful')

    def delete(self, entity, node, protocol="netconf", provider_proto='default'):
        """Invoke a crud.create for a given entity on a node using the specified protocol.

        """

        # Open up the provider session if necessary
        self._open_provider_session(node, protocol, provider_proto)

        # Initiate a crud.create on the selected provider

        self._crud.delete(self._session, entity)

        logger.debug('Crud Delete Successful')
