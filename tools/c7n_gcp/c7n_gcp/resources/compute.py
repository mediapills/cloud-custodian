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

from c7n_gcp.actions import MethodAction, SetIamPolicy
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


@resources.register('node-template')
class NodeTemplate(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/nodeTemplates
   """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'nodeTemplates'
        enum_spec = ('aggregatedList', 'items.*.nodeTemplates[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'region': resource_info['region'],
                        'nodeTemplate': resource_info['resourceName'].rsplit('/', 1)[-1]})


@NodeTemplate.action_registry.register('delete')
class NodeTemplateDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/compute/docs/reference/rest/v1/nodeTemplates/delete>`_
    a Node Template. The action does not specify any parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-node-template-delete
            resource: gcp.node-template
            filters:
              - type: value
                key: name
                value: node-template-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        project, region, node_template = re.match(
            '.*/projects/(.*?)/regions/(.*?)/nodeTemplates/(.*)', r['selfLink']).groups()
        return {'project': project, 'region': region, 'nodeTemplate': node_template}


@NodeTemplate.action_registry.register('set-iam-policy')
class NodeTemplateSetIamPolicy(SetIamPolicy):

    def _verb_arguments(self, resource):
        """
        Overrides the base implementation to process Node Template resources correctly.
        """
        project, region, resource = re.match('.*/projects/(.+?)/regions/(.+?)/nodeTemplates/(.+)',
                                             resource['selfLink']).groups()
        return {'project': project, 'region': region, 'resource': resource}
