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

from c7n.utils import local_session, type_schema
from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo, \
    GcpLocation


@resources.register('kms-keyring')
class KmsKeyRing(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'cloudkms'
        version = 'v1'
        component = 'projects.locations.keyRings'
        enum_spec = ('list', 'keyRings[]', None)
        scope = None
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            name = 'projects/{}/locations/{}/keyRings/{}' \
                .format(resource_info['project_id'],
                        resource_info['location'],
                        resource_info['key_ring_id'])
            return client.execute_command('get', {'name': name})

    def get_resource_query(self):
        if 'query' in self.data:
            for child in self.data.get('query'):
                if 'location' in child:
                    location_query = child['location']
                    return {'parent': location_query if isinstance(
                        location_query, list) else [location_query]}

    def _fetch_resources(self, query):
        super_fetch_resources = QueryResourceManager._fetch_resources
        session = local_session(self.session_factory)
        project = session.get_default_project()
        locations = (query['parent'] if query and 'parent' in query
                     else GcpLocation.get_service_locations('kms'))
        project_locations = ['projects/{}/locations/{}'.format(project, location)
                             for location in locations]
        key_rings = []
        for location in project_locations:
            key_rings.extend(super_fetch_resources(self, {'parent': location}))
        return key_rings


@resources.register('kms-cryptokey')
class KmsCryptoKey(ChildResourceManager):

    def _get_parent_resource_info(self, child_instance):
        project_id, location, key_ring_id = re.match(
            'projects/(.*?)/locations/(.*?)/keyRings/(.*?)/cryptoKeys/.*',
            child_instance['name']).groups()
        return {'project_id': project_id,
                'location': location,
                'key_ring_id': key_ring_id}

    def get_resource_query(self):
        """Does nothing as self does not need query values unlike its parent
        which receives them with the use_child_query flag."""
        pass

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
            ],
            'use_child_query': True
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
        path = 'projects/(.*?)/locations/(.*?)/keyRings/(.*?)/cryptoKeys/(.*?)/cryptoKeyVersions/.*'
        project_id, location, key_ring_id, crypto_key_id = \
            re.match(path, child_instance['name']).groups()
        return {'project_id': project_id,
                'location': location,
                'key_ring_id': key_ring_id,
                'crypto_key_id': crypto_key_id}

    def get_resource_query(self):
        """Does nothing as self does not need query values unlike its parent
        which receives them with the use_child_query flag."""
        pass

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
            ],
            'use_child_query': True
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


@KmsCryptoKeyVersion.action_registry.register('destroy')
class KmsCryptoKeyVersionDestroy(MethodAction):
    """The action is used for kms crypto key version destroy.

    GCP action is https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/destroy

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-kms-cryptokey-version-destroy
            resource: gcp.kms-cryptokey-version
            filters:
              - type: value
                key: protectionLevel
                op: not-in
                value: [SOFTWARE, HSM]
            actions:
              - type: destroy
    """
    schema = type_schema('destroy')
    method_spec = {'op': 'destroy'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@KmsCryptoKeyVersion.action_registry.register('restore')
class KmsCryptoKeyVersionRestore(MethodAction):
    """The action is used for kms crypto key version restore.

    GCP action is https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/restore

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-kms-cryptokey-version-restore
            resource: gcp.kms-cryptokey-version
            filters:
              - type: value
                key: protectionLevel
                op: in
                value: [SOFTWARE, HSM]
            actions:
              - type: restore
    """
    schema = type_schema('restore')
    method_spec = {'op': 'restore'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@KmsCryptoKeyVersion.action_registry.register('set')
class KmsCryptoKeyVersionSet(MethodAction):
    """The action is used for kms crypto key version set.

    GCP action is https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/patch

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-kms-cryptokey-version-set
            resource: gcp.kms-cryptokey-version
            filters:
              - type: value
                key: protectionLevel
                op: in
                value: [SOFTWARE, HSM]
            actions:
              - type: set
                state: ENABLED
    """
    schema = type_schema('set',
                         **{'state': {
                             'type': 'string',
                             'enum': [
                                 "CRYPTO_KEY_VERSION_STATE_UNSPECIFIED",
                                 "PENDING_GENERATION", "ENABLED",
                                 "DISABLED", "DESTROYED", "DESTROY_SCHEDULED",
                                 "PENDING_IMPORT", "IMPORT_FAILED"
                             ]
                         }})
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'name': resource['name'],
            'updateMask': 'state',
            'body': {'state': self.data['state']}
        }
