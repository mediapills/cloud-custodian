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

from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo


@resources.register('container-location-cluster')
class ContainerLocationCluster(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations.clusters'
        enum_spec = ('list', 'clusters[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}/locations/-'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/clusters/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['cluster'])})


@resources.register('container-zone')
class ContainerZone(QueryResourceManager):

    def resources(self, query=None):
        raise NotImplementedError('Action list not implemented for resource projects.zones')

    class resource_type(TypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.zones'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'getServerconfig', verb_arguments={
                    'projectId': resource_info['project_id'],
                    'zone': resource_info['zone']})


@resources.register('container-location')
class ContainerLocation(QueryResourceManager):

    def resources(self, query=None):
        raise NotImplementedError('Action list not implemented for resource projects.locations')

    class resource_type(TypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'getServerConfig', verb_arguments={
                    'name': 'projects/{}/locations/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'])})
