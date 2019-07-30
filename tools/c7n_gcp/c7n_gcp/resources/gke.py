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
class KubernetesCluster(QueryResourceManager):
    """GCP resource:
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters
    """

    class resource_type(TypeInfo):
        service = 'container'
        version = 'v1'
        component = 'projects.locations.clusters'
        enum_spec = ('list', 'clusters[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = "projects/{}/locations/-"
        id = "name"

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/clusters/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['cluster_name'])})


@KubernetesCluster.action_registry.register('delete')
class KubernetesClusterActionDelete(MethodAction):
    """The action is used for GKE projects.locations.clusters delete.
    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters
    /delete

    Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-delete-biggest
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

        return {"name": name}


@KubernetesCluster.action_registry.register('set-resource-labels')
class KubernetesClusterActionSetResourceLabels(MethodAction):
    """The action is used for GKE projects.locations.clusters setResourceLabels.
    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters
    /setResourceLabels

    Example:

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
                    - key: nodes
                      value: minimal
    """

    schema = type_schema(
        'set-resource-labels',
        **{
            'labels': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'key': {'type': 'string'},
                        'value': {'type': 'string'}
                    }
                }
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
                'resourceLabels': {
                    k: v for k, v in self.data['labels']
                }
            }}


@KubernetesCluster.action_registry.register('update')
class KubernetesClusterActionUpdate(MethodAction):
    """The action is used for GKE projects.locations.clusters update node version.
    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters
    /update

    Example:

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
                nodeversion: "1.13.6-gke.13"
    """

    schema = type_schema(
        'update',
        **{
            'nodeversion': {
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

        return {
            'name': name,
            'body': {
                'update': {
                    "desiredMasterVersion": self.data['nodeversion']
                }
            }}


@resources.register('gke-nodepool')
class KubernetesClusterNodePool(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1
    /projects.zones.clusters.nodePools
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
                r".*{}-(.*)-[^-]+-[^-]?".format(cluster_name),
                resource_info['resourceName']).group(1)

            return client.execute_command(
                'get', verb_arguments={
                    'name': 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(
                        resource_info['project_id'],
                        resource_info['location'],
                        resource_info['cluster_name'],
                        name)}
            )


@KubernetesClusterNodePool.action_registry.register('set-autoscaling')
class KubernetesClusterNodePoolSetActionAutoscaling(MethodAction):
    """The action is used for GKE projects.zones.clusters.nodePools autoscaling setup.
    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools
    /autoscaling

    Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-nodepool-set-autoscaling
            resource: gcp.gke-nodepool
            filters:
              - type: value
                key: initialNodeCount
                value: 3
            actions:
              - type: set-autoscaling
                enabled: true
                minNodeCount: 3
                maxNodeCount: 3
    """

    schema = type_schema(
        'set-autoscaling',
        **{
            'autoscaling': {
                'type': 'string'
            },
            'minNodeCount': {
                'type': 'string'
            },
            'maxNodeCount': {
                'type': 'string'
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

        if self.data['autoscaling']:
            params = {
                "enabled": "true",
                "minNodeCount": self.data['minNodeCount'],
                "maxNodeCount": self.data['maxNodeCount']
            }
        else:
            params = {"enabled": "false"}

        return {
            'name': name,
            'body': {
                "autoscaling": params
            }}


@KubernetesClusterNodePool.action_registry.register('set-size')
class KubernetesClusterNodePoolSetActionSetSize(MethodAction):
    """The action is used for GKE projects.zones.clusters.nodePools size setup.
    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1
    /projects.zones.clusters.nodePools/setSize

    Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-nodepool-set-size
            resource: gcp.gke-nodepool
            filters:
              - type: value
                key: initialNodeCount
                value: 4
                op: greater-than
            actions:
              - type: set
                node-count: 3
    """

    schema = type_schema(
        'set-size',
        **{
            'node-count': {
                'type': 'string'
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
                "nodeCount": self.data['node-count']
            }}


@KubernetesClusterNodePool.action_registry.register('set-management')
class KubernetesClusterNodePoolSetActionManagement(MethodAction):
    """The action is used for GKE projects.zones.clusters.nodePools management setup.
    GCP action is
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1
    /projects.zones.clusters.nodePools/setManagement

    Example:

    .. code-block:: yaml

        policies:
          - name: gke-cluster-nodepool-set-auto-upgrade
            resource: gcp.gke-nodepool
            actions:
              - type: set-management
                autoUpgrade: true
    """

    schema = type_schema(
        'set-management',
        **{
            'upgrade': {
                'type': 'string'
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
                "management": {
                    "autoUpgrade": self.data['upgrade']
                }
            }}
