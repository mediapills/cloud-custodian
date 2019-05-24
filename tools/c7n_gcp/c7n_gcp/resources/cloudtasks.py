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

import jmespath, re

from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo
from c7n.utils import local_session


@resources.register('cloudtasks-location')
class CloudTasksLocation(QueryResourceManager):
    """GCP resource: https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations
    This one is present only as the parent of other resources.
    """
    def get_resource_query(self):
        return {'name': 'projects/%s' % local_session(self.session_factory).get_default_project()}

    class resource_type(TypeInfo):
        service = 'cloudtasks'
        version = 'v2'
        component = 'projects.locations'
        enum_spec = ('list', 'locations[]', None)
        scope = None
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query('get', {'name': resource_info['name']})


@resources.register('cloudtasks-queue')
class CloudTasksQueue(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues
    """
    def _get_child_enum_args(self, parent_instance):
        return {'parent': parent_instance['name']}

    def _get_parent_resource_info(self, child_instance):
        return {'name': re.match('(projects/.*?/locations/.*?)/queues/.*',
                                 child_instance['name']).group(1)}

    class resource_type(ChildTypeInfo):
        service = 'cloudtasks'
        version = 'v2'
        component = 'projects.locations.queues'
        enum_spec = ('list', 'queues[]', None)
        scope = None
        get_requires_event = True
        id = 'name'
        parent_spec = {
            'resource': 'cloudtasks-location'
        }

        @staticmethod
        def get(client, event):
            return client.execute_query(
                'get', {'name': jmespath.search('protoPayload.response.name', event)})


@resources.register('cloudtasks-task')
class CloudTask(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues.tasks
    """
    def _get_child_enum_args(self, parent_instance):
        return {'parent': parent_instance['name']}

    def _get_parent_resource_info(self, child_instance):
        return {'protoPayload': {'response': {
            'name': re.match('(projects/.*?/locations/.*?/queues/.*?)/tasks/.*',
                             child_instance['name']).group(1)}}}

    class resource_type(ChildTypeInfo):
        service = 'cloudtasks'
        version = 'v2'
        component = 'projects.locations.queues.tasks'
        enum_spec = ('list', 'tasks[]', None)
        scope = None
        id = 'name'
        parent_spec = {
            'resource': 'cloudtasks-queue'
        }

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', {'name': resource_info['resourceName']})
