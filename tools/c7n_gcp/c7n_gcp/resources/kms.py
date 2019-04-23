# Copyright 2019 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo


@resources.register('kms-location')
class KmsLocation(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'cloudkms'
        version = 'v1'
        component = 'projects.locations'
        enum_spec = ('list', 'locations[]', None)
        scope = 'project'
        scope_key = 'name'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            name = 'projects/{}/locations/{}'.format(
                resource_info['project_id'], resource_info['location'])
            return client.execute_command('get', {'name': name})


@resources.register('kms-keyring')
class KmsKeyRing(ChildResourceManager):

    def _get_parent_resource_info(self, child_instance):
        param_re = re.compile('projects/(.*?)/locations/(.*?)/keyRings/.*?')
        project_id, location = param_re.match(child_instance['name']).groups()
        return {'project_id': project_id,
                'location': location}

    class resource_type(ChildTypeInfo):
        service = 'cloudkms'
        version = 'v1'
        component = 'projects.locations.keyRings'
        enum_spec = ('list', 'keyRings[]', None)
        scope = None
        id = 'name'
        parent_spec = {
            'resource': 'kms-location',
            'child_enum_params': [
                ('name', 'parent')
            ]
        }

        @staticmethod
        def get(client, resource_info):
            name = 'projects/{}/locations/{}/keyRings/{}' \
                .format(resource_info['project_id'],
                        resource_info['location'],
                        resource_info['key_ring_id'])
            return client.execute_command('get', {'name': name})


@resources.register('kms-cryptokey')
class KmsCryptoKey(ChildResourceManager):

    def _get_parent_resource_info(self, child_instance):
        param_re = re.compile('projects/(.*?)/locations/(.*?)/keyRings/(.*?)/cryptoKeys/.*')
        project_id, location, key_ring_id = param_re.match(child_instance['name']).groups()
        return {'project_id': project_id,
                'location': location,
                'key_ring_id': key_ring_id}

    class resource_type(ChildTypeInfo):
        service = 'cloudkms'
        version = 'v1'
        component = 'projects.locations.keyRings.cryptoKeys'
        enum_spec = ('list', 'cryptoKeys[]', None)
        scope = None
        id = 'name'
        parent_spec = {
            'resource': 'kms-keyring',
            'child_enum_params': [
                ('name', 'parent')
            ]
        }

        @staticmethod
        def get(client, resource_info):
            name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}' \
                .format(resource_info['project_id'],
                        resource_info['location'],
                        resource_info['key_ring_id'],
                        resource_info['crypto_key_id'])
            return client.execute_command('get', {'name': name})


@resources.register('kms-cryptokey-version')
class KmsCryptoKeyVersion(ChildResourceManager):

    def _get_parent_resource_info(self, child_instance):
        param_re = re.compile(
            'projects/(.*?)/locations/(.*?)/keyRings/(.*?)/cryptoKeys/(.*?)/cryptoKeyVersions/.*')
        project_id, location, key_ring_id, crypto_key_id =\
            param_re.match(child_instance['name']).groups()
        return {'project_id': project_id,
                'location': location,
                'key_ring_id': key_ring_id,
                'crypto_key_id': crypto_key_id}

    class resource_type(ChildTypeInfo):
        service = 'cloudkms'
        version = 'v1'
        component = 'projects.locations.keyRings.cryptoKeys.cryptoKeyVersions'
        enum_spec = ('list', 'cryptoKeyVersions[]', None)
        scope = None
        id = 'name'
        parent_spec = {
            'resource': 'kms-cryptokey',
            'child_enum_params': [
                ('name', 'parent')
            ]
        }

        @staticmethod
        def get(client, resource_info):
            name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}/cryptoKeyVersions/{}'\
                .format(resource_info['project_id'],
                        resource_info['location'],
                        resource_info['key_ring_id'],
                        resource_info['crypto_key_id'],
                        resource_info['crypto_key_version_id'])
            return client.execute_command('get', {'name': name})
