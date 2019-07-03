# Copyright 2018-2019 Capital One Services, LLC
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
from c7n.utils import type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo


@resources.register('project-role')
class ProjectRole(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'iam'
        version = 'v1'
        component = 'projects.roles'
        enum_spec = ('list', 'roles[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = "name"

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', verb_arguments={
                    'name': 'projects/{}/roles/{}'.format(
                        resource_info['project_id'],
                        resource_info['role_name'].rsplit('/', 1)[-1])})


@ProjectRole.action_registry.register('delete')
class ProjectRoleActionDelete(MethodAction):
    """The action is used for IAM projects.roles delete.
    GCP resource is https://cloud.google.com/bigquery/docs/reference/rest/v2/projects.roles.
    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/projects.roles/delete
    Example:
    .. code-block:: yaml
         policies:
          - name: gcp-iam-project-role
            resource: gcp.project-role
            filters:
              - type: value
                key: title
                value: Custom Role
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ProjectRole.action_registry.register('update-title')
class ProjectRoleActionPatch(MethodAction):
    """The action is used for IAM projects.roles name patch.
    GCP resource is https://cloud.google.com/bigquery/docs/reference/rest/v2/projects.roles.
    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/projects.roles/patch
    Example:
    .. code-block:: yaml
        policies:
          - name: gcp-iam-project-role-update-title
            resource: gcp.project-role
            filters:
              - type: value
                key: title
                value: Custom Role
            actions:
              - type: update-title
                name: CustomRole1
    """

    schema = type_schema(
        'update-title',
        **{
            'type': {'enum': ['update-title']},
            'title': {'type': 'string'}
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'name': resource['name'],
            'body': {'title': self.data['title']}
        }


@resources.register('service-account')
class ServiceAccount(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'iam'
        version = 'v1'
        component = 'projects.serviceAccounts'
        enum_spec = ('list', 'accounts[]', [])
        scope = 'project'
        scope_key = 'name'
        scope_template = 'projects/{}'
        id = "name"

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', verb_arguments={
                    'name': 'projects/{}/serviceAccounts/{}'.format(
                        resource_info['project_id'],
                        resource_info['email_id'])})


@ServiceAccount.action_registry.register('set-iam-policy')
class ServiceAccountSetIamPolicy(MethodAction):
    """Sets IAM policy. It works with bindings only.
    GCP resource is https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts.
    GCP action is
    https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/setIamPolicy.
    Example:
    .. code-block:: yaml
        policies:
        - name: gcp-iam-service-account-set-iam-policy
          resource: gcp.service-account
          actions:
          - type: set-iam-policy
            bindings:
            - members:
              - user:user1@test.com
              - user2@test.com
              role: roles/owner
            - members:
              - user:user3@gmail.com
              role: roles/viewer
    """
    schema = type_schema('setIamPolicy',
                         required=['bindings'],
                         **{
                             'type': {'enum': ['set-iam-policy']},
                             'bindings': {
                                 'type': 'array',
                                 'items': {'role': {'type': 'string'}, 'members': {'type': 'array'}}
                             }
                         }
                         )
    method_spec = {'op': 'setIamPolicy'}

    MEMBER_TYPES = ['user', 'group', 'domain', 'serviceAccount']

    def get_resource_params(self, model, resource):
        result = {'resource': resource['name'],
                  'body': {
                      'policy': {
                          'bindings': []
                      }}
                  }
        bindings = result['body']['policy']['bindings']

        if self.data['bindings'] is not None:
            for binding in self.data['bindings']:
                if binding['role'] and binding['members']:
                    members = []
                    for member in binding['members']:
                        requires_update = True
                        for member_type in self.MEMBER_TYPES:
                            if member.startswith(member_type + ':'):
                                requires_update = False
                                break
                        if requires_update:
                            member = 'user:' + member
                        members.append(member)
                    bindings.append({'role': binding['role'], 'members': members})

        return result


@resources.register('iam-role')
class Role(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'iam'
        version = 'v1'
        component = 'roles'
        enum_spec = ('list', 'roles[]', None)
        scope = "global"
        id = "name"

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {
                    'name': 'roles/{}'.format(
                        resource_info['name'])})
