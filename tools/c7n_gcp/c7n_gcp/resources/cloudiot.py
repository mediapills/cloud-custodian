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

from c7n.utils import type_schema
from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo
from c7n.utils import local_session


@resources.register('cloudiot-registry')
class CloudIotRegistry(QueryResourceManager):

    def get_resource_query(self):
        if 'query' in self.data:
            project_id = local_session(self.session_factory).get_default_project()
            location_id = self.data.get('query')[0]['location']
            return {'parent': 'projects/{}/locations/{}'.format(project_id, location_id)}

    class resource_type(TypeInfo):
        service = 'cloudiot'
        version = 'v1'
        component = 'projects.locations.registries'
        enum_spec = ('list', 'deviceRegistries[]', None)
        scope = None
        id = 'id'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', {'name': resource_info['resourceName']})


@CloudIotRegistry.action_registry.register('delete')
class CloudIotRegistryDelete(MethodAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        return {'name': r['name']}


@resources.register('cloudiot-device')
class CloudIotDevice(ChildResourceManager):

    def get_resource_query(self):
        return {}

    def get_parent_resource_query(self):
        if 'query' in self.data:
            return self.data.get('query')

    def _get_parent_resource_info(self, child_instance):
        return {'resourceName': re.match(
            '(projects/.*?/locations/.*?/registries/.*?)/devices/.*',
            child_instance['name']).group(1)}

    class resource_type(ChildTypeInfo):
        service = 'cloudiot'
        version = 'v1'
        component = 'projects.locations.registries.devices'
        enum_spec = ('list', 'devices[]', None)
        scope = None
        id = 'id'
        parent_spec = {
            'resource': 'cloudiot-registry',
            'child_enum_params': [
                ('name', 'parent')
            ]
        }

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', {'name': resource_info['resourceName']})
