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

# TODO .. folder, billing account, org sink
# how to map them given a project level root entity sans use of c7n-org


@resources.register('log-sink')
class LogSink(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'projects.sinks'
        enum_spec = ('list', 'sinks[]', None)
        scope_key = 'parent'
        scope_template = "projects/{}"
        id = "name"

        @staticmethod
        def get(client, resource_info):
            return client.execute_query('get', {
                'sinkName': 'projects/{project_id}/sinks/{name}'.format(
                    **resource_info)})


@resources.register('log-project-sink')
class LogProjectSink(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'projects.sinks'
        enum_spec = ('list', 'sinks[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query('get', {
                'sinkName': 'projects/{project_id}/sinks/{name}'.format(
                    **resource_info)})


@resources.register('log-project-metric')
class LogProjectMetric(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'projects.metrics'
        enum_spec = ('list', 'metrics[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query('get', {
                'metricName': 'projects/{project_id}/metrics/{name}'.format(
                    **resource_info)})


@resources.register('log-project')
class LogProject(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'projects.logs'
        enum_spec = ('list', 'logNames[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'project_id'

    def augment(self, resources):
        out_resources = []
        for resource in resources:
            resource_type, project_id, key, log_id = resource.split('/')
            out_resources.append({
                'logName ': resource,
                'resource_type': resource_type,
                'project_id': project_id,
                'key': key,
                'log_id': log_id
            })
        return out_resources


@resources.register('log-project-exclusion')
class LogProjectExclusion(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'projects.exclusions'
        enum_spec = ('list', 'exclusions[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query('get', {
                'name': 'projects/{project_id}/exclusions/{exclusion_id}'.format(
                    **resource_info)})


@resources.register('log-exclusion')
class LogExclusion(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'exclusions'
        enum_spec = ('list', 'exclusions[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query('get', {
                'name': '{type}/{project_id}/exclusions/{exclusion_id}'.format(
                    **resource_info)})


@resources.register('log-monitored-resource-descriptor')
class LogMonitoredResourceDescriptor(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'monitoredResourceDescriptors'
        enum_spec = ('list', 'resourceDescriptors[]', None)
        scope = 'global'
        id = 'name'


@resources.register('log-entries')
class LogEntries(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'logging'
        version = 'v2'
        component = 'entries'
        enum_spec = ('list', 'entries[]', None)
        id = "name"
        scope = None


    def get_resource_query(self):
        if 'query' in self.data:
            return {'body': {'resourceNames': [self.data.get('query')]}}