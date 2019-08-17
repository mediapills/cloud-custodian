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

from c7n.exceptions import PolicyExecutionError
from c7n.utils import type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo


@resources.register('vpc-access-policy')
class VpcAccessPolicy(QueryResourceManager):
    """GCP resource:
    https://cloud.google.com/access-context-manager/docs/reference/rest/v1/accessPolicies
    """
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
                    if 'organization_id' in element:
                        scope_key = self.resource_type.scope_key
                        scope_template = self.resource_type.scope_template
                        result_query[scope_key] = scope_template.format(element['organization_id'])
        return result_query


@VpcAccessPolicy.action_registry.register('delete')
class VpcAccessPolicyDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/access-context-manager/docs/reference/rest/v1
    /accessPolicies/delete>`_ a VPC access policy

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-vpc-access-policies-delete
            resource: gcp.vpc-access-level
            query:
              - organization_id: 926683928810
            filters:
              - type: value
                key: parent
                op: eq
                value: organizations/926683928810
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


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
        id = 'name'
        parent_spec = {
            'resource': 'vpc-access-policy',
            'child_enum_params': [
                ('name', 'parent')
            ],
            'parent_get_params': [
                ('parent', 'parent')],
            'use_child_query': True
        }

    def get_resource_query(self):
        """Does nothing as self does not need query values unlike its parent
        which receives them with the use_child_query flag."""
        pass


@VpcAccessLevel.action_registry.register('delete')
class VpcAccessLevelDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/access-context-manager/docs/reference/rest/v1
    /accessPolicies.accessLevels/delete>`_ a VPC access level

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-vpc-access-levels-delete
            resource: gcp.vpc-access-level
            query:
              - organization_id: 926683928810
            filters:
              - type: value
                key: title
                op: contains
                value: dev
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@VpcAccessLevel.action_registry.register('set')
class VpcAccessLevelSet(MethodAction):
    """
    `Patches <https://cloud.google.com/access-context-manager/docs/reference/rest/v1
    /accessPolicies.accessLevels/patch>`_ a VPC access level

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-vpc-access-levels-patch
            resource: gcp.vpc-access-level
            query:
              - organization_id: 926683928810
            filters:
              - type: value
                key: title
                op: contains
                value: admin
            actions:
              - type: set
                description: new description
                basic:
                  conditions:
                    - regions:
                        - BY
                        - US
                        - RU
    """
    schema = type_schema('patch',
                         **{'type': {'enum': ['set']},
                            'title': {'type': 'string'},
                            'description': {'type': 'string'},
                            'basic': {
                                'type': 'object',
                                'conditions': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'negate': {'type': 'boolean'},
                                        'ipSubnetworks': {
                                            'type': 'array',
                                            'items': {'type': 'string'}},
                                        'devicePolicy': {
                                            'type': 'array',
                                            'items': {'type': 'string'}},
                                        'requiredAccessLevels': {
                                            'type': 'array',
                                            'items': {'type': 'string'}},
                                        'members': {
                                            'type': 'array',
                                            'items': {'type': 'string'}},
                                        'regions': {
                                            'type': 'array',
                                            'items': {'type': 'string'}}}}}})
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        data = self.data
        available_properties = self.schema['properties']
        intersection_set = set(data.keys()) & set(available_properties)
        update_mask = []
        body = {}
        for element in intersection_set:
            if element != 'type':
                body[element] = data[element]
                update_mask.append(element)
        if not update_mask:
            raise PolicyExecutionError('The updating fields are absent')
        result = {'name': resource['name'],
                  'updateMask': ','.join(update_mask),
                  'body': body}
        return result


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
        id = 'name'
        parent_spec = {
            'resource': 'vpc-access-policy',
            'child_enum_params': [
                ('name', 'parent')
            ],
            'parent_get_params': [
                ('parent', 'parent')],
            'use_child_query': True
        }

    def get_resource_query(self):
        """Does nothing as self does not need query values unlike its parent
        which receives them with the use_child_query flag."""
        pass


@VpcServicePerimeter.action_registry.register('delete')
class VpcServicePerimeterDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/access-context-manager/docs/reference/rest/v1
    /accessPolicies.servicePerimeters/delete>`_ a VPC service perimeter

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-vpc-service-perimeter-delete
            resource: gcp.vpc-service-perimeter
            query:
              - organization_id: 926683928810
            filters:
              - type: value
                key: status.accessLevels
                op: contains
                value: accessPolicies/1016634752304/accessLevels/custodian_viewer
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@VpcServicePerimeter.action_registry.register('set')
class VpcServicePerimeterSet(MethodAction):
    """
    `Patches <https://cloud.google.com/access-context-manager/docs/reference/rest/v1
    /accessPolicies.servicePerimeters/patch>`_ a VPC service perimeter

    Example:

    .. code-block:: yaml

        policies:
          - name: gcp-vpc-service-perimeters-patch
            resource: gcp.vpc-service-perimeter
            query:
              - organization_id: 926683928810
            filters:
              - type: value
                key: status.accessLevels
                op: contains
                value: accessPolicies/1016634752304/accessLevels/custodian_viewer
            actions:
              - type: set
                description: new description
                status:
                  resources:
                    - projects/test-project-123
                    - projects/test-project-321
                  accessLevels:
                    - accessPolicies/1016634752304/accessLevels/custodian_viewer
                    - accessPolicies/1016634752304/accessLevels/custodian_viewer_2
                  restrictedServices:
                    - bigquery.googleapis.com
                    - pubsub.googleapis.com
    """
    schema = type_schema('patch',
                         **{'type': {'enum': ['set']},
                            'title': {'type': 'string'},
                            'description': {'type': 'string'},
                            'status': {
                                'type': 'object',
                                'description': {'type': 'string'},
                                'resources': {'type': 'array', 'items': {'type': 'string'}},
                                'accessLevels': {'type': 'array', 'items': {'type': 'string'}},
                                'restrictedServices': {'type': 'array',
                                                       'items': {'type': 'string'}}}})
    method_spec = {'op': 'patch'}
    project_not_found_message_template = 'Unable to match a project number for the ' \
                                         'following project id: {}.'

    def get_resource_params(self, model, resource):
        data = self.data
        available_properties = self.schema['properties']
        intersection_set = set(data.keys()) & set(available_properties)
        update_mask = []
        body = {}
        for element in intersection_set:
            if element != 'type':
                body[element] = data[element]
                update_mask.append(element)
            if element == 'status' and 'resources' in body['status']:
                body['status']['resources'] = self._prepare_status_resources_param(
                    body['status']['resources']
                )

        if not update_mask:
            raise PolicyExecutionError('The updating fields are absent')
        result = {'name': resource['name'],
                  'updateMask': ','.join(update_mask),
                  'body': body}
        return result

    def _prepare_status_resources_param(self, status_resources):
        projects = self.manager.get_resource_manager('project').resources()
        updated_resources = []

        for r in status_resources:
            if r.startswith('projects'):
                r = 'projects/{}'.format(
                    self._find_project_id(projects, r.rsplit('/', 1)[1])
                )
            updated_resources.append(r)

        return updated_resources

    def _find_project_id(self, projects, project_id):
        matched_project = next((p for p in projects if p['projectId'] == project_id), None)

        if not matched_project:
            raise ValueError(self.project_not_found_message_template.format(project_id))

        return matched_project['projectNumber']
