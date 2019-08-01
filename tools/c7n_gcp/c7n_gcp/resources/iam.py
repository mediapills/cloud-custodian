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
    """ GCP resource is https://cloud.google.com/iam/reference/rest/v1/projects.roles
    """
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
    GCP action is https://cloud.google.com/iam/reference/rest/v1/projects.roles/delete

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


@ProjectRole.action_registry.register('set')
class ProjectRoleActionPatch(MethodAction):
    """The action is used for IAM projects.roles name patch.
    GCP action is https://cloud.google.com/iam/reference/rest/v1/projects.roles/patch

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
              - type: set
                title: CustomRole1
    """

    schema = type_schema(
        'set',
        **{
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
    """ GCP resource is https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts
    """
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


@ServiceAccount.action_registry.register('delete')
class ServiceAccountActionDelete(MethodAction):
    """The action is used for IAM projects.serviceAccounts delete.
    GCP action is https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/delete

    Example:
    .. code-block:: yaml
        policies:
          - name: gcp-iam-service-account-delete
            resource: gcp.service-account
            filters:
              - type: value
                key: name
                value: projects/{project}/serviceAccounts/{acountid}
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ServiceAccount.action_registry.register('disable')
class ServiceAccountActionDisable(MethodAction):
    """The action is used for IAM projects.serviceAccounts disable.
    GCP action is https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/disable

    Example:
    .. code-block:: yaml
        policies:
          - name: gcp-iam-service-account-disable
            resource: gcp.service-account
            filters:
              - type: value
                key: name
                value: projects/{project}/serviceAccounts/{acountid}
            actions:
              - type: disable
    """

    schema = type_schema('disable')
    method_spec = {'op': 'disable'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ServiceAccount.action_registry.register('enable')
class ServiceAccountActionEnable(MethodAction):
    """The action is used for IAM projects.serviceAccounts enable.
    GCP action is https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/enable

    Example:
    .. code-block:: yaml
        policies:
          - name: gcp-iam-service-account-enable
            resource: gcp.service-account
            filters:
              - type: value
                key: name
                value: projects/{project}/serviceAccounts/{acountid}
            actions:
              - type: enable
    """

    schema = type_schema('enable')
    method_spec = {'op': 'enable'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ServiceAccount.action_registry.register('set')
class ServiceAccountActionSetDisplayName(MethodAction):
    """The action is used for IAM projects.serviceAccounts set display name.
    GCP action is https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/patch

    Example:
    .. code-block:: yaml
        policies:
          - name: gcp-iam-service-account-set
            resource: gcp.service-account
            filters:
              - type: value
                key: name
                value: projects/{project}/serviceAccounts/{acountid}
            actions:
              - type: set
                display_name: test-name
    """

    schema = type_schema(
        'set',
        **{
            'display_name': {'type': 'string'}
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'name': resource['name'],
            'body': {
                  "serviceAccount": {
                    "displayName": self.data['display_name']
                  },
                  "updateMask": "displayName"
                }
        }


@resources.register('iam-role')
class Role(QueryResourceManager):
    """ GCP resource is https://cloud.google.com/iam/reference/rest/v1/roles
    """
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
