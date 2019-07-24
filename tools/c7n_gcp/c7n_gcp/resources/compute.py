# Copyright 2017-2018 Capital One Services, LLC
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

from c7n.utils import type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo

from c7n.filters.offhours import OffHour, OnHour


@resources.register('instance')
class Instance(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'instances'
        enum_spec = ('aggregatedList', 'items.*.instances[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            # The api docs for compute instance get are wrong,
            # they spell instance as resourceId
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'zone': resource_info['zone'],
                        'instance': resource_info[
                            'resourceName'].rsplit('/', 1)[-1]})


@Instance.filter_registry.register('offhour')
class InstanceOffHour(OffHour):

    def get_tag_value(self, instance):
        return instance.get('labels', {}).get(self.tag_key)


@Instance.filter_registry.register('onhour')
class InstanceOnHour(OnHour):

    def get_tag_value(self, instance):
        return instance.get('labels', {}).get(self.tag_key)


class InstanceAction(MethodAction):

    def get_resource_params(self, model, resource):
        project, zone, instance = self.path_param_re.match(
            resource['selfLink']).groups()
        return {'project': project, 'zone': zone, 'instance': instance}


@Instance.action_registry.register('start')
class Start(InstanceAction):

    schema = type_schema('start')
    method_spec = {'op': 'start'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')
    attr_filter = ('status', ('TERMINATED',))


@Instance.action_registry.register('stop')
class Stop(InstanceAction):

    schema = type_schema('stop')
    method_spec = {'op': 'stop'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')
    attr_filter = ('status', ('RUNNING',))


@Instance.action_registry.register('delete')
class Delete(InstanceAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')


@resources.register('image')
class Image(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'images'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'resourceId': resource_info['image_id']})


@Image.action_registry.register('delete')
class DeleteImage(MethodAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    attr_filter = ('status', ('READY'))
    path_param_re = re.compile('.*?/projects/(.*?)/global/images/(.*)')

    def get_resource_params(self, m, r):
        project, image_id = self.path_param_re.match(r['selfLink']).groups()
        return {'project': project, 'image': image_id}


@resources.register('disk')
class Disk(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'disks'
        scope = 'zone'
        enum_spec = ('aggregatedList', 'items.*.disks[]', None)
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'zone': resource_info['zone'],
                        'resourceId': resource_info['disk_id']})


@Disk.action_registry.register('snapshot')
class DiskSnapshot(MethodAction):

    schema = type_schema('snapshot')
    method_spec = {'op': 'createSnapshot'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')
    attr_filter = ('status', ('RUNNING',))


@resources.register('snapshot')
class Snapshot(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'snapshots'
        enum_spec = ('list', 'items[]', None)
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'snapshot_id': resource_info['snapshot_id']})


@Snapshot.action_registry.register('delete')
class DeleteSnapshot(MethodAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    attr_filter = ('status', ('READY', 'UPLOADING'))
    path_param_re = re.compile('.*?/projects/(.*?)/global/snapshots/(.*)')

    def get_resource_params(self, m, r):
        project, snapshot_id = self.path_param_re.match(r['selfLink']).groups()
        # Docs are wrong :-(
        # https://cloud.google.com/compute/docs/reference/rest/v1/snapshots/delete
        return {'project': project, 'snapshot': snapshot_id}


@resources.register('gce-security-policy')
class GceSecurityPolicy(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/securityPolicies"""
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'securityPolicies'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'securityPolicy': resource_info['policy_name']})


@GceSecurityPolicy.action_registry.register('delete')
class DeleteGceSecurityPolicy(MethodAction):
    """`Deletes <https://cloud.google.com/compute/docs/reference/rest/v1/securityPolicies/delete>`_
    a security policy
    Example:

    .. code-block:: yaml

        policies:
          - name: gce-security-policy-delete
            description: Deletes a security policy
            resource: gcp.gce-security-policy
            filters:
               - type: value
                 key: name
                 value: test-policy
            actions:
               - delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    path_param_re = re.compile('.*?/projects/(.*?)/global/securityPolicies/(.*)')

    def get_resource_params(self, m, r):
        project, policy = self.path_param_re.match(r['selfLink']).groups()
        return {'project': project, 'securityPolicy': policy}


@GceSecurityPolicy.action_registry.register('add-rule')
class AddRuleGceSecurityPolicy(MethodAction):
    """
    `Inserts <https://cloud.google.com/compute/docs/reference/rest/v1/securityPolicies/addRule>`_
    a rule into a security policy.
    The 'action' specifies the action to perform when the client connection triggers the rule. Can
    currently be either "allow" or "deny()" where valid values for status are 403, 404, 502.
    The 'srcIpRanges' specifies CIDR IP address range.
    The 'priority' specifies the priority of a rule in the list.
    Example:

    .. code-block:: yaml

        policies:
          - name: gcp-gce-security-policy-add-rule
            resource: gcp.gce-security-policy
            actions:
              - type: add-rule
                action: deny(403)
                srcIpRanges: ['66.77.88.0/24']
                priority: 0
    """
    schema = type_schema('add-rule',
                         **{
                             'action': {
                                 'type': {'enum': ['allow', 'deny(403)', 'deny(404)', 'deny(502)']}
                             },
                             'srcIpRanges': {
                                 'type': 'array',
                                 'items': {'type': 'string'}
                             },
                             'priority': {
                                 'type': 'integer',
                                 'minimum': 0,
                                 'maximum': 2147483647
                             }
                         })
    method_spec = {'op': 'addRule'}
    path_param_re = re.compile('.*?/projects/(.*?)/global/securityPolicies/(.*)')

    def get_resource_params(self, model, resource):
        project, policy = self.path_param_re.match(resource['selfLink']).groups()

        result = {'project': project,
                  'securityPolicy': policy,
                  'body': {
                      'action': self.data['action'],
                      'match': {
                          'config': {
                              'srcIpRanges': self.data['srcIpRanges']
                          },
                          'versionedExpr': 'SRC_IPS_V1'
                      },
                      'priority': self.data['priority']
                  }}

        return result