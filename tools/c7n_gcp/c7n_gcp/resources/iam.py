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
class ProjectRoleDelete(MethodAction):
    """`Deletes <https://cloud.google.com/iam/reference/rest/v1/projects.roles/delete>`_
    IAM projects.roles. The action does not specify additional parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-iam-project-role
            resource: gcp.project-role
            filters:
              - type: value
                key: title
                op: contains
                value: Custom Role
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ProjectRole.action_registry.register('set')
class ProjectRoleSet(MethodAction):
    """`Patches <https://cloud.google.com/iam/reference/rest/v1/projects.roles/patch>`_
    IAM projects.roles.

    The required `includedPermissions` parameter accepts an array of strings that represent `IAM
    Permissions <https://cloud.google.com/iam/docs/permissions-reference>`_. The new permissions
    overwrite the existing ones.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-iam-project-role-set-permissions
            resource: gcp.project-role
            filters:
              - type: value
                key: title
                op: contains
                value: executor
            actions:
              - type: set
                includedPermissions:
                  - appengine.services.delete
                  - accessapproval.requests.approve
    """
    schema = type_schema(
        'set',
        required=['includedPermissions'],
        **{
            'includedPermissions': {
                'type': 'array',
                'items': {'type': 'string'}
            }
        }
    )
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'name': resource['name'],
            'body': {
                'title': resource['title'],
                'includedPermissions': self.data['includedPermissions']
            }
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
class ServiceAccountDelete(MethodAction):
    """`Deletes <https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/delete>`_
    IAM projects.serviceAccounts. The action does not specify additional parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-iam-service-account-delete
            resource: gcp.service-account
            filters:
              - type: value
                key: email
                op: regex
                value: ^special[a-zA-Z0-9_]+@cloudcustodian\.io$ # noqa: W605
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ServiceAccount.action_registry.register('disable')
class ServiceAccountDisable(MethodAction):
    """`Disables <https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/disable>`_
    IAM projects.serviceAccounts. The action does not specify additional parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-iam-service-account-disable
            resource: gcp.service-account
            filters:
              - type: value
                key: displayName
                op: not-in
                value: [accounting, privacy, confidential]
            actions:
              - type: disable
    """
    schema = type_schema('disable')
    method_spec = {'op': 'disable'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ServiceAccount.action_registry.register('enable')
class ServiceAccountEnable(MethodAction):
    """`Enables <https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/enable>`_
    IAM projects.serviceAccounts. The action does not specify additional parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-iam-service-account-enable
            resource: gcp.service-account
            filters:
              - type: value
                key: displayName
                op: in
                value: [accounting, privacy, confidential]
            actions:
              - type: enable
    """
    schema = type_schema('enable')
    method_spec = {'op': 'enable'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@ServiceAccount.action_registry.register('set')
class ServiceAccountSet(MethodAction):
    """`Patches <https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts/patch>`_
    IAM projects.serviceAccounts.

    The available string parameters are `description` and `displayName`, at least one of which
    is mandatory to be set in a policy. The `description` parameter is a user-specified opaque
    description of the service account that must be less than or equal to 256 UTF-8 bytes.
    `displayName` is a user-specified name for the service account not bigger than 100 UTF-8 bytes.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-iam-service-account-set
            resource: gcp.service-account
            filters:
              - type: value
                key: email
                op: in
                value: [sample1@email, sample2@email, sample3@email]
            actions:
              - type: set
                description: checked by Custodian
                displayName: checked by Custodian
    """
    schema = type_schema(
        'set',
        **{
            'minProperties': 1,
            'additionalProperties': False,
            'description': {'type': 'string'},
            'displayName': {'type': 'string'}
        }
    )
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        fields = ['description', 'displayName']
        body = {key: self.data[key] for key in fields if key in self.data}
        return {
            'name': resource['name'],
            'body': {
                'serviceAccount': body,
                'updateMask': ','.join(body.keys())
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
