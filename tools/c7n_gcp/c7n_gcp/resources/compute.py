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


@resources.register('instance-template')
class InstanceTemplate(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/instanceTemplates"""
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'instanceTemplates'
        scope = 'zone'
        enum_spec = ('list', 'items[]', None)
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'instanceTemplate': resource_info['instance_template_name']})


@InstanceTemplate.action_registry.register('delete')
class InstanceTemplateDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/compute/docs/reference/rest/v1/instanceTemplates/delete>`_
    an Instance Template. The action does not specify any parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-instance-template-delete
            resource: gcp.instance-template
            filters:
              - type: value
                key: name
                value: instance-template-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        project, instance_template = re.match('.*/projects/(.*?)/.*/instanceTemplates/(.*)',
                                              r['selfLink']).groups()
        return {'project': project,
                'instanceTemplate': instance_template}


@resources.register('instance-group-manager')
class InstanceGroupManager(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/instanceGroupManagers
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'instanceGroupManagers'
        enum_spec = ('aggregatedList', 'items.*.instanceGroupManagers[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'zone': resource_info['location'],
                        'instanceGroupManager': resource_info['instance_group_manager_name']})


@InstanceGroupManager.action_registry.register('delete')
class InstanceGroupManagerDelete(MethodAction):
    """`Deletes <https://cloud.google.com/compute/docs/reference/rest/v1/instanceGroupManagers
    /delete>`_ an instance group manager

    :Example:

    .. code-block:: yaml

        policies:
          - name: instance-group-manager-delete
            resource: gcp.instance-group-manager
            filters:
              - type: value
                key: name
                op: eq
                value: test-instance-group
            actions:
              - delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    path_param_re = re.compile('.*?/projects/(.*?)/zones/(.*?)/instanceGroupManagers/(.*)')

    def get_resource_params(self, m, r):
        project, zone, name = self.path_param_re.match(r['selfLink']).groups()
        return {'project': project, 'zone': zone, 'instanceGroupManager': name}


@InstanceGroupManager.action_registry.register('set')
class InstanceGroupManagerSet(MethodAction):
    """
    `Patches <https://cloud.google.com/compute/docs/reference/rest/v1/instanceGroupManagers
    /patch>`_ configuration parameters for an instance group.

    The `instanceTemplate` represents an URL of the instance template that is specified for
    this managed instance group.

    The `autoHealingPolicies[].healthCheck` represents an URL for the health check that
    signals autohealing.

    The `autoHealingPolicies[]` specifies the autohealing policy for this managed instance group.
    You can specify only one value.

    The `autoHealingPolicies[].initialDelaySec` specifies the  number of seconds that the managed
    instance group waits before it applies autohealing policies to new instances or recently
    recreated instances.

    The `updatePolicy.type` specifies the type of update process. You can specify either
    'PROACTIVE' so that the instance group manager proactively executes actions in order to bring
    instances to their target versions or 'OPPORTUNISTIC' so that no action is proactively executed
    but the update will be performed as part of other actions.

    The `updatePolicy.minimalAction` specifies minimal action to be taken on an instance.  You
    can specify either 'RESTART' to restart existing instances or 'REPLACE' to delete and create
    new instances from the target template.

    The `updatePolicy.maxSurge.fixed` specifies a fixed number of VM instances. This must be a
    positive integer.
    The `updatePolicy.maxSurge.percent` specifies a percentage of instances between 0 to 100%,
    inclusive. For example, specify 80 for 80%.

    The `updatePolicy.maxUnavailable.fixed` specifies a fixed number of VM instances. This must be
    a positive integer.

    The `updatePolicy.maxUnavailable.percent` specifies a percentage of instances between 0 to
    100%, inclusive. For example, specify 80 for 80%.

    :Example:

    .. code-block:: yaml

        policies:
          - name: instance-group-manager-set
            resource: gcp.instance-group-manager
            actions:
              - type: set
                instanceTemplate:
                  "https://www.googleapis.com/compute/v1/projects/mitrop-custodian\
                  /global/instanceTemplates/instance-template-2"
                autoHealingPolicies:
                  - healthCheck:
                      "https://www.googleapis.com/compute/v1/projects/mitrop-custodian/global\
                      /healthChecks/test-health-check"
                    initialDelaySec: 10
                updatePolicy:
                  type: OPPORTUNISTIC
                  minimalAction: REPLACE
                  maxSurge:
                    fixed: 4
                  maxUnavailable:
                    fixed: 1
    """
    schema = type_schema('set',
                         **{
                             'instanceTemplate': {'type': 'string'},
                             'autoHealingPolicies': {
                                 'type': 'array',
                                 'items': {
                                     'type': 'object',
                                     'required': ['healthCheck'],
                                     'properties': {
                                         'healthCheck': {'type': 'string'},
                                         'initialDelaySec': {
                                             'type': 'integer',
                                             'maximum': 3600,
                                             'minimum': 0
                                         }
                                     }
                                 },
                             },
                             'updatePolicy': {
                                 'type': 'object',
                                 'properties': {
                                     'type': {
                                         'type': 'string',
                                         'enum': ['PROACTIVE', 'OPPORTUNISTIC']
                                     },
                                     'minimalAction': {
                                         'type': 'string',
                                         'enum': ['RESTART', 'REPLACE']
                                     },
                                     'maxSurge': {
                                         'type': 'object',
                                         'properties': {
                                             'fixed': {
                                                 'type': 'integer',
                                                 'minimum': 0
                                             },
                                             'percent': {
                                                 'type': 'integer',
                                                 'maximum': 100,
                                                 'minimum': 0
                                             }
                                         }
                                     },
                                     'maxUnavailable': {
                                         'type': 'object',
                                         'properties': {
                                             'fixed': {
                                                 'type': 'integer',
                                                 'minimum': 0
                                             },
                                             'percent': {
                                                 'type': 'integer',
                                                 'maximum': 100,
                                                 'minimum': 0
                                             }
                                         }
                                     }
                                 }
                             }
                         })
    method_spec = {'op': 'patch'}
    path_param_re = re.compile('.*?/projects/(.*?)/zones/(.*?)/instanceGroupManagers/(.*)')

    def get_resource_params(self, model, resource):
        project, zone, manager = self.path_param_re.match(resource['selfLink']).groups()
        body = {}

        if 'instanceTemplate' in self.data:
            body['instanceTemplate'] = self.data['instanceTemplate']

        if 'autoHealingPolicies' in self.data:
            body['autoHealingPolicies'] = self.data['autoHealingPolicies']

        if 'updatePolicy' in self.data:
            body['updatePolicy'] = self.data['updatePolicy']

        result = {'project': project,
                  'zone': zone,
                  'instanceGroupManager': manager,
                  'body': body}

        return result
