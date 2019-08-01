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

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo

from c7n.filters.offhours import OffHour, OnHour
from c7n.utils import local_session, type_schema


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


@resources.register('gce-node-group')
class GceNodeGroup(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'nodeGroups'
        enum_spec = ('aggregatedList', 'items.*.nodeGroups[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'zone': resource_info['zone'],
                        'nodeGroup': resource_info['resourceName'].rsplit('/', 1)[-1]})


@GceNodeGroup.action_registry.register('delete')
class GceNodeGroupDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups/delete>`_
    a Node Group. The action does not specify any parameters.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-gce-node-group-delete
            resource: gcp.gce-node-group
            filters:
              - type: value
                key: name
                value: node-group-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        project, zone, node_group = re.match(
            '.*/projects/(.*?)/zones/(.*?)/nodeGroups/(.*)', r['selfLink']).groups()
        return {'project': project, 'zone': zone, 'nodeGroup': node_group}


class GceNodeGroupChangeSizeAction(MethodAction):
    def _get_project_zone_node_group(self, r):
        return re.match('.*/projects/(.*?)/zones/(.*?)/nodeGroups/(.*)', r['selfLink']).groups()

    def _get_current_size(self, r):
        return r['size']

    def _get_target_size(self):
        return self.data['target-size']


@GceNodeGroup.action_registry.register('increase-size')
class GceNodeGroupIncreaseSize(GceNodeGroupChangeSizeAction):
    """
    `Adds Nodes
    <https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups/addNodes>`_
    to a Node Group.

    The required 'target-size' parameter must be greater than the current Node size, otherwise
    the `target_not_greater_than_current_error` `ValueError` is raised. As it is possible
    to have a Node Group without nodes (0), the schema specifies the next possible value (1)
    as the minimal one.

    Behind the scenes, the `_get_additional_node_count` method defines the number of the Nodes
    to add that will be further used as a parameter in the API call.

    .. code-block:: yaml

        policies:
          - name: gcp-gce-node-group-increase-size-from-1-to-2
            resource: gcp.gce-node-group
            filters:
              - type: value
                key: size
                op: greater-than
                value: 1
            actions:
              - type: decrease-size
                target-size: 2
    """
    schema = type_schema('increase-size',
                         **{
                             'additionalProperties': False,
                             'required': ['target-size'],
                             'target-size': {
                                 'type': 'integer',
                                 'minimum': 1  # if current size is 0
                             }
                         })
    method_spec = {'op': 'addNodes'}
    min_target_size = 2
    target_not_greater_than_current_error = 'Target node group size (%d) ' \
                                            'must be greater than the current (%s)'

    def get_resource_params(self, m, r):
        project, zone, node_group = self._get_project_zone_node_group(r)
        return {'project': project, 'zone': zone, 'nodeGroup': node_group,
                'body': {'additionalNodeCount': self._get_additional_node_count(r)}}

    def _get_additional_node_count(self, r):
        """
        Validates `target_size` (T) against the `current_size` (C)
        and returns the T - C difference.

        :param r: the same as in `get_resource_params`
        :return: a positive integer
        :raises ValueError: if T <= C
        """
        current_size = self._get_current_size(r)
        target_size = self._get_target_size()
        if target_size <= current_size:
            raise ValueError(self.target_not_greater_than_current_error %
                             (target_size, current_size))
        return target_size - current_size


@GceNodeGroup.action_registry.register('decrease-size')
class GceNodeGroupDecreaseSize(GceNodeGroupChangeSizeAction):
    """
    `Deletes Nodes
    <https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups/deleteNodes>`_
    from a Node Group.

    The required 'target-size' parameter must be smaller than the current Node size, otherwise
    the `target_not_smaller_than_current_error` `ValueError` is raised. As it is possible
    to have a Node Group without nodes, the schema specifies 0 as the minimal value.

    Behind the scenes, the `_get_nodes_to_delete` method defines the names of the Nodes to delete
    that will be further used as a parameter in the API call.

    .. code-block:: yaml

        policies:
          - name: gcp-gce-node-group-decrease-size-from-2-to-1
            resource: gcp.gce-node-group
            filters:
              - type: value
                key: size
                op: greater-than
                value: 2
            actions:
              - type: decrease-size
                target-size: 1
    """
    schema = type_schema('decrease-size',
                         **{
                             'additionalProperties': False,
                             'required': ['target-size'],
                             'target-size': {
                                 'type': 'integer',
                                 'minimum': 0  # if current size is 1
                             }
                         })
    method_spec = {'op': 'deleteNodes'}
    min_target_size = 1
    target_not_smaller_than_current_error = 'Target node group size (%d) ' \
                                            'must be smaller than the current (%s)'

    def get_resource_params(self, m, r):
        project, zone, node_group = self._get_project_zone_node_group(r)
        return {'project': project, 'zone': zone, 'nodeGroup': node_group,
                'body': {'nodes': self._get_nodes_to_delete(r)}}

    def _get_nodes_to_delete(self, r):
        """
        Validates `target_size` (T) against the `current_size` (C), calculates the difference
        (D = C - T) and returns the list of the names of the `nodes
        <https://cloud.google.com/compute/docs/reference/rest/v1/nodeGroups/listNodes>`_
        except for the D nodes left out from the end of the list.

        :param r: the same as in `get_resource_params`
        :return: a non-empty list of Node names
        :raises ValueError: if T >= C
        """
        project, zone, node_group = self._get_project_zone_node_group(r)
        current_size = self._get_current_size(r)
        target_size = self._get_target_size()
        if target_size >= current_size:
            raise ValueError(self.target_not_smaller_than_current_error %
                             (target_size, current_size))
        m = self.manager.get_model()
        session = local_session(self.manager.session_factory)
        client = self.get_client(session, m)
        current_nodes = client.execute_command('listNodes', {
            'project': project,
            'zone': zone,
            'nodeGroup': node_group
        })
        return [node['name'] for node in current_nodes['items'][(current_size - target_size):]]
