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
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo


@resources.register('vpc-access-policy')
class VpcAccessPolicy(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'accesscontextmanager'
        version = 'v1'
        component = 'accessPolicies'
        enum_spec = ('list', 'accessPolicies[]', None)
        scope = None
        scope_key = 'parent'
        scope_template = 'organizations/{}'
        id = 'name'

    def get_resource_query(self):
        result_query = {}
        result_query['parent'] = {}
        if 'query' in self.data:
            query = self.data.get('query')
            if query is not None:
                for element in query:
                    if element.__contains__('organization_id'):
                        scope_key = self.resource_type.scope_key
                        scope_template = self.resource_type.scope_template
                        result_query[scope_key] = scope_template.format(element['organization_id'])
        return result_query


@resources.register('vpc-access-level')
class VpcAccessLevel(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'accesscontextmanager'
        version = 'v1'
        component = 'accessPolicies.accessLevels'
        enum_spec = ('list', 'accessLevels[]', None)
        scope = None
        scope_key = 'parent'
        scope_template = 'organizations/{}'
        parent_spec = {
            'resource': 'vpc-access-policy',
            'child_enum_params': [
                ('name', 'parent')
            ],
            'parent_get_params': [
                ('parent', 'parent')]
        }

    def get_resource_query(self):
        return

    def get_parent_resource_query(self):
        result_query = [{'organization_id': None}]
        if 'query' in self.data:
            query = self.data.get('query')
            if query is not None:
                for element in query:
                    if element.__contains__('organization_id'):
                        result_query[0]['organization_id'] = element['organization_id']
        return result_query


@resources.register('vpc-service-perimeter')
class VpcServicePerimeter(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'accesscontextmanager'
        version = 'v1'
        component = 'accessPolicies.servicePerimeters'
        enum_spec = ('list', 'servicePerimeters[]', None)
        scope = None
        scope_key = 'parent'
        scope_template = 'organizations/{}'
        parent_spec = {
            'resource': 'vpc-access-policy',
            'child_enum_params': [
                ('name', 'parent')
            ],
            'parent_get_params': [
                ('parent', 'parent')]
        }

    def get_resource_query(self):
        return

    def get_parent_resource_query(self):
        result_query = [{'organization_id': None}]
        if 'query' in self.data:
            query = self.data.get('query')
            if query is not None:
                for element in query:
                    if element.__contains__('organization_id'):
                        result_query[0]['organization_id'] = element['organization_id']
        return result_query
