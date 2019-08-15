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


@Instance.action_registry.register('enforce-tags')
class EnforceTags(InstanceAction):
    """
    The `Set Tags <https://cloud.google.com/compute/docs/reference/rest/v1/instances/setTags>`_
    action controls what tags must be present or absent on a VM Instance.

    The `add-tags` parameter accepts a list of hyphen-separated alphanumeric strings that,
    if absent, will be added while preserving the existing ones. Namely, no action will be taken
    if all the specified tags are already present.

    The `remove-tags` parameter accepts a list of hyphen-separated alphanumeric strings that will
    be removed from the resulting list. The tags that are removed already are simply ignored.
    In addition, the parameter accepts the '*' value which is treated as removing all the tags.

    Not that specifying the same tag both in `add-tags` and `remove-tags` (not a recommended thing
    to do but still possible) results in having no tag in the resulting list.

    :example:

    .. code-block:: yaml

    policies:
      - name: gce-compute-enforce-tags
        resource: gcp.instance
        filters:
          - type: value
            key: name
            value: instance-whose-tags-to-enforce
        actions:
          - type: enforce-tags
            add-tags:
              - tag-to-add-one
              - tag-to-add-two
            remove-tags:
              - tag-to-remove
    """
    schema = type_schema(
        'enforce-tags',
        **{
            'minProperties': 1,
            'additionalProperties': False,
            'add-tags': {'type': 'array',
                         'items': {'type': 'string',
                                   'pattern': '^[a-z0-9]+(-[a-z0-9]+)*$'}},
            'remove-tags': {'oneOf': [
                {'type': 'array',
                 'items': {'type': 'string',
                           'pattern': '^[a-z0-9]+(-[a-z0-9]+)*$'}},
                {'enum': ['*']}
            ]}
        })
    method_spec = {'op': 'setTags'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/zones/(.*?)/instances/(.*)')

    def get_resource_params(self, model, resource):
        params = InstanceAction.get_resource_params(self, model, resource)
        instance_tags = resource['tags']
        if self._should_remove_all_tags():
            tags_to_enforce = []
        else:
            existing_tags = instance_tags['items'] if 'items' in instance_tags else []
            tags_to_enforce = self._filter_existing_tags(self._extend_existing_tags(existing_tags))
        params['body'] = {'items': tags_to_enforce, 'fingerprint': instance_tags['fingerprint']}
        return params

    def _should_remove_all_tags(self):
        """
        Returns `True` if the value at the `remove-tags` key in self.data is a string representation
        of an asterisk ('*') which in its turn implies that an empty array of tags has to be used.
        """
        return 'remove-tags' in self.data and self.data['remove-tags'] == '*'

    def _extend_existing_tags(self, existing_tags):
        """
        Returns a copy of the provided `existing_tags` which has been extended with all the items
        from the list at the `add-tags` key in `self.data`.

        :param existing_tags: a list a copy of which to extend and return
        """
        tags_to_add = self.data['add-tags'] if 'add-tags' in self.data else []
        updated_tags = list(existing_tags)
        updated_tags.extend([tag for tag in tags_to_add if tag not in existing_tags])
        return updated_tags

    def _filter_existing_tags(self, existing_tags):
        """
        Returns a copy of the provided `existing_tags` which has been filtered against all the items
        from the list at the `remove-tags` key in `self.data`.

        :param existing_tags: a list a copy of which to filter and return
        """
        tags_to_remove = self.data['remove-tags'] if 'remove-tags' in self.data else []
        updated_tags = list(existing_tags)
        return list(filter(lambda a: a not in tags_to_remove, updated_tags))


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
