# Copyright 2018 Capital One Services, LLC
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

from c7n_gcp.provider import resources
from c7n_gcp.query import (QueryResourceManager, TypeInfo, ChildTypeInfo,
                           ChildResourceManager)
from c7n.utils import local_session, type_schema
from c7n_gcp.actions import MethodAction


@resources.register('gke-cluster')
class GKECluster(QueryResourceManager):
    """GCP resource:
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters
    """

    class resource_type(TypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations.clusters'
        enum_spec = ('list', 'clusters[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = 'projects/{}/locations/-'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/clusters/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['cluster_name'])})


@GKECluster.action_registry.register('delete')
class GKEClusterDelete(MethodAction):
    """The action is used for GKE projects.locations.clusters delete.

    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters
    /delete

    :Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-delete-large
            resource: gcp.gke-cluster
            filters:
              - type: value
                key: currentNodeCount
                value: 3
                op: gt
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        session = local_session(self.manager.session_factory)
        name = 'projects/{}/locations/{}/clusters/{}'.format(
            session.get_default_project(),
            resource['locations'][0],
            resource['name'])

        return {'name': name}


@GKECluster.action_registry.register('set-resource-labels')
class GKEClusterSetResourceLabels(MethodAction):
    """The action is used for GKE projects.locations.clusters set resource labels.

    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters
    /setResourceLabels

    :Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-set-label-for-small
            resource: gcp.gke-cluster
            filters:
              - type: value
                key: currentNodeCount
                value: 3
            actions:
              - type: set-resource-labels
                labels:
                  nodes: minimal
    """

    schema = type_schema(
        'set-resource-labels',
        required=['labels'],
        **{
            'labels': {
                'type': 'object'
            }
        }
    )

    method_spec = {'op': 'setResourceLabels'}

    def get_resource_params(self, model, resource):
        session = local_session(self.manager.session_factory)
        name = 'projects/{}/locations/{}/clusters/{}'.format(
            session.get_default_project(),
            resource['locations'][0],
            resource['name'])

        return {
            'name': name,
            'body': {
                'resourceLabels': self.data['labels']
            }}


@GKECluster.action_registry.register('update')
class GKEClusterUpdate(MethodAction):
    """The action is used for GKE projects.locations.clusters update.

    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters
    /update

    :Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-update-node-version
            resource: gcp.gke-cluster
            filters:
              - type: value
                key: currentNodeVersion
                value: 1.12.8-gke.10
            actions:
              - type: update
                nodeversion: 1.13.6-gke.13
    """

    schema = type_schema(
        'update',
        **{
            'nodeversion': {
                'type': 'string'
            },
            'monitoring-service': {
                'type': 'string'
            }
        }
    )

    method_spec = {'op': 'update'}

    def get_resource_params(self, model, resource):
        session = local_session(self.manager.session_factory)
        name = 'projects/{}/locations/{}/clusters/{}'.format(
            session.get_default_project(),
            resource['locations'][0],
            resource['name'])

        params = {}

        if 'nodeversion' in self.data:
            params['desiredMasterVersion'] = self.data['nodeversion']

        if 'monitoring-service' in self.data:
            params['desiredMonitoringService'] = self.data['monitoring-service']

        return {
            'name': name,
            'body': {
                'update': params
            }}


@resources.register('gke-cluster-nodepool')
class GKEClusterNodePool(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1
    /projects.locations.clusters.nodePools
    """

    def _get_parent_resource_info(self, child_instance):
        project_param_re = re.compile(
            '.*?/projects/(.*?)/zones/(.*?)/clusters/(.*?)/nodePools/(.*?)'
        )
        parent_values = re.match(project_param_re, child_instance['selfLink']).groups()
        parent_info = dict(
            zip(('project_id', 'location', 'cluster_name', 'node_name'), parent_values)
        )

        return parent_info

    def _get_child_enum_args(self, parent_instance):
        return {
            'parent': 'projects/{}/locations/{}/clusters/{}'.format(
                local_session(self.session_factory).get_default_project(),
                parent_instance['location'],
                parent_instance['name']
            )
        }

    class resource_type(ChildTypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations.clusters.nodePools'
        enum_spec = ('list', 'nodePools[]', None)
        scope = 'global'
        id = 'name'
        parent_spec = {'resource': 'gke-cluster'}

        @staticmethod
        def get(client, resource_info):
            cluster_name = resource_info['cluster_name']
            name = re.match(
                r'.*{}-(.*)-[^-]+-[^-]?'.format(cluster_name),
                resource_info['resourceName']).group(1)

            return client.execute_command(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['cluster_name'],
                        name)}
            )


@GKEClusterNodePool.action_registry.register('set-autoscaling')
class GKEClusterNodePoolSetAutoscaling(MethodAction):
    """The action is used for GKE projects.locations.clusters.nodePools autoscaling setup.

    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/
    projects.locations.clusters.nodePools/setAutoscaling

    :Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-nodepool-set-autoscaling
            resource: gcp.gke-cluster-nodepool
            filters:
              - type: value
                key: initialNodeCount
                value: 3
            actions:
              - type: set-autoscaling
                enabled: true
                min-node-count: 3
                max-node-count: 3
    """

    schema = type_schema(
        'set-autoscaling',
        required=['enabled'],
        **{
            'enabled': {
                'type': 'boolean'
            },
            'min-node-count': {
                'type': 'integer'
            },
            'max-node-count': {
                'type': 'integer'
            }
        }
    )

    method_spec = {'op': 'setAutoscaling'}

    def get_resource_params(self, model, resource):
        session = local_session(self.manager.session_factory)
        key = self.manager.resource_type.get_parent_annotation_key()

        name = 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(
            session.get_default_project(),
            resource[key]['locations'][0],
            resource[key]['name'],
            resource['name'])

        params = {'enabled': 'true' if 'enabled' in self.data else 'false'}

        if 'enabled' in self.data:
            if 'min-node-count' in self.data:
                params['minNodeCount'] = self.data['min-node-count']
            if 'max-node-count' in self.data:
                params['maxNodeCount'] = self.data['max-node-count']

        return {
            'name': name,
            'body': {
                'autoscaling': params
            }}


@GKEClusterNodePool.action_registry.register('set-size')
class GKEClusterNodePoolSetSize(MethodAction):
    """The action is used for GKE projects.locations.clusters.nodePools size setup.

    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/
    projects.locations.clusters.nodePools/setSize

    :Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-nodepool-set-size
            resource: gcp.gke-cluster-nodepool
            filters:
              - type: value
                key: initialNodeCount
                value: 4
                op: greater-than
            actions:
              - type: set-size
                node-count: 3
    """

    schema = type_schema(
        'set-size',
        required=['node-count'],
        **{
            'node-count': {
                'type': 'integer'
            }
        }
    )

    method_spec = {'op': 'setSize'}

    def get_resource_params(self, model, resource):
        session = local_session(self.manager.session_factory)
        key = self.manager.resource_type.get_parent_annotation_key()

        name = 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(
            session.get_default_project(),
            resource[key]['locations'][0],
            resource[key]['name'],
            resource['name'])

        return {
            'name': name,
            'body': {
                'nodeCount': self.data['node-count']
            }}


@GKEClusterNodePool.action_registry.register('set-management')
class GKEClusterNodePoolSetManagement(MethodAction):
    """The action is used for GKE projects.locations.clusters.nodePools management setup.

    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/
    projects.locations.clusters.nodePools/setManagement

    :Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-nodepool-set-auto-upgrade
            resource: gcp.gke-cluster-nodepool
            actions:
              - type: set-management
                auto-upgrade: true
    """

    schema = type_schema(
        'set-management',
        required=['auto-upgrade'],
        **{
            'auto-upgrade': {
                'type': 'boolean'
            }
        }
    )

    method_spec = {'op': 'setManagement'}

    def get_resource_params(self, model, resource):
        session = local_session(self.manager.session_factory)
        key = self.manager.resource_type.get_parent_annotation_key()

        name = 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(
            session.get_default_project(),
            resource[key]['locations'][0],
            resource[key]['name'],
            resource['name'])

        return {
            'name': name,
            'body': {
                'management': {
                    'autoUpgrade': self.data['auto-upgrade']
                }
            }}
