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
import re

from c7n_gcp.provider import resources
from c7n_gcp.query import (QueryResourceManager, TypeInfo, ChildTypeInfo,
                           ChildResourceManager)
from c7n.utils import local_session


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


@resources.register('gke-cluster-nodepool')
class KubernetesClusterNodePool(ChildResourceManager):

    def __get_mappings(self, self_link, mapping_dict):
        mappings = {}
        project_param_re = re.compile(
            '.*?/projects/(.*?)/zones/(.*?)/clusters/(.*?)/nodePools/(.*?)'
        )
        for key, value in mapping_dict.items():
            mappings[key] = project_param_re.match(self_link).group(value)
        return mappings

    def _get_parent_resource_info(self, child_instance):
        mapping_dict = {
            'project_id': 1,
            'location': 2,
            'cluster_name': 3,
            'node_name': 4
        }
        return self.__get_mappings(child_instance['selfLink'], mapping_dict)

    def _get_child_enum_args(self, parent_instance):
        parent_instance['parent_path'] = 'projects/{}/locations/{}/clusters/{}'.format(
            local_session(self.session_factory).get_default_project(),
            parent_instance['location'],
            parent_instance['name']
        )
        return super(KubernetesClusterNodePool, self)._get_child_enum_args(parent_instance)

    class resource_type(ChildTypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations.clusters.nodePools'
        enum_spec = ('list', 'nodePools[]', None)
        scope = 'global'
        id = 'name'
        parent_spec = {
            'resource': 'gke-cluster',
            'child_enum_params': [
                ('parent_path', 'parent')
            ],
        }

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['cluster_name'],
                        resource_info['node_name'])}
            )
