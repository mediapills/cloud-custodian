# Copyright 2018 Capital One Services, LLC
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


@resources.register('gke-cluster')
class KubernetesCluster(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations.clusters'
        enum_spec = ('list', 'clusters[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = "projects/{}/locations/-"
        id = "name"

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/clusters/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['cluster_name'])})


@resources.register('gke-operation')
class KubernetesOperation(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations.operations'
        enum_spec = ('list', 'operations[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = 'projects/{}/locations/-'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/operations/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['operation_name'])})
