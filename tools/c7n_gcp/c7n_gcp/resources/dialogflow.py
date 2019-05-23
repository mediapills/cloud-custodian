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


@resources.register('dialogflow-agent')
class DialogFlowAgent(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'dialogflow'
        version = 'v2'
        component = 'projects.agent'
        enum_spec = ('search', 'agents[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['location'],
                'address': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('dialogflow-entity-type')
class DialogFlowEntityType(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'dialogflow'
        version = 'v2'
        component = 'projects.agent.entityTypes'
        enum_spec = ('list', 'entityTypes[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}/agent'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['location'],
                'address': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('dialogflow-intent')
class DialogFlowIntent(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'dialogflow'
        version = 'v2'
        component = 'projects.agent.intents'
        enum_spec = ('list', 'intents[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}/agent'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['location'],
                'address': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('dialogflow-session-context')
class DialogFlowSessionContext(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'dialogflow-enterprise'
        version = 'v2'
        component = 'projects.agents'
        enum_spec = ('search', 'instances[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['location'],
                'address': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('dialogflow-session-entity-type')
class DialogFlowSessionEntityType(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'dialogflow-enterprise'
        version = 'v2'
        component = 'projects.agents'
        enum_spec = ('search', 'instances[]', None)
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['location'],
                'address': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})