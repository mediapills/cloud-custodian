# Copyright 2019 Capital One Services, LLC
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
import json
import os
import time
from gcp_common import BaseTest, event_data


class GKEClusterTest(BaseTest):

    def test_cluster_query(self):
        project_id = "cloud-custodian"

        factory = self.replay_flight_data('gke-cluster-query', project_id)
        p = self.load_policy(
            {'name': 'all-gke-cluster',
             'resource': 'gcp.gke-cluster'},
            session_factory=factory
        )
        resources = p.run()
        self.assertEqual(resources[0]['status'], 'RUNNING')
        self.assertEqual(resources[0]['name'], 'standard-cluster-1')

    def test_cluster_get(self):
        project_id = "cloud-custodian"
        name = "standard-cluster-1"

        factory = self.replay_flight_data('gke-cluster-get', project_id)

        p = self.load_policy({
            'name': 'one-gke-cluster',
            'resource': 'gcp.gke-cluster',
            'mode': {
                'type': 'gcp-audit',
                'methods': ['io.k8s.core.v1.nodes.create']}},
            session_factory=factory)

        exec_mode = p.get_execution_mode()
        event = event_data('k8s_create_cluster.json')
        clusters = exec_mode.run(event, None)

        self.assertEqual(clusters[0]['name'], name)

    def test_cluster_set_label(self):
        project_id = "cloud-custodian"

        factory = self.replay_flight_data('gke-cluster-set-label', project_id)

        base_policy = {'name': 'gke-cluster-set-label',
                       'resource': 'gcp.gke-cluster',
                       'filters': [{
                           'type': 'value',
                           'key': 'currentNodeCount',
                           'value': 3
                       }]}

        p = self.load_policy(
            dict(base_policy,
                 actions=[{
                     'type': 'set-resource-labels',
                     'labels': [{
                         'key': 'nodes',
                         'value': 'minimal'
                     }]
                 }]),
            session_factory=factory)

        resources = p.run()

        self.assertEqual(resources[0]['resourceLabels'], {'nodes': 'minimal'})

    def test_cluster_update(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('gke-cluster-update-node-version', project_id=project_id)

        p = self.load_policy(
            {'name': 'set-cluster-node-version',
             'resource': 'gcp.gke-cluster',
             'actions': [{
                 'type': 'update',
                 'nodeversion': "1.12.8-gke.10"
             }]},
            session_factory=factory)

        resources = p.run()
        self.assertEqual(len(resources), 1)

        if self.recording:
            time.sleep(10)

        client = p.resource_manager.get_client()
        result = client.execute_query('list', {
            'parent': 'projects/{}/locations/-'.format(project_id)})

        self.assertEqual(result['clusters'][0]['status'], 'RECONCILING')

    def test_cluster_delete(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('gke-cluster-delete', project_id=project_id)

        p = self.load_policy(
            {'name': 'gke-cluster-delete',
             'resource': 'gcp.gke-cluster',
             'actions': [{
                 'type': 'delete'
             }]},
            session_factory=factory)

        resources = p.run()
        self.assertEqual(len(resources), 1)

        if self.recording:
            time.sleep(10)

        client = p.resource_manager.get_client()
        result = client.execute_query('list', {
            'parent': 'projects/{}/locations/-'.format(project_id)})

        self.assertEqual(result['clusters'][0]['status'], 'STOPPING')


class KubernetesClusterNodePoolTest(BaseTest):

    def test_cluster_node_pools_query(self):
        project_id = "cloud-custodian"

        factory = self.replay_flight_data('gke-cluster-nodepool-query', project_id)

        p = self.load_policy(
            {'name': 'all-gke-nodepools',
             'resource': 'gcp.gke-nodepool'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(resources[0]['status'], 'RUNNING')
        self.assertEqual(resources[0]['name'], 'default-pool')

    def test_cluster_node_pools_get(self):

        project_id = "cloud-custodian"
        name = "pool-1"

        factory = self.replay_flight_data('gke-cluster-nodepool-get', project_id)

        p = self.load_policy(
            {
                'name': 'one-gke-nodepool',
                'resource': 'gcp.gke-nodepool',
                'mode': {
                    'type': 'gcp-audit',
                    'methods': ['io.k8s.core.v1.pods.create']
                }
            }, session_factory=factory)

        exec_mode = p.get_execution_mode()
        event = event_data('k8s_create_pool.json')
        pools = exec_mode.run(event, None)

        self.assertEqual(pools[0]['name'], name)

    def test_cluster_node_pools_set_autoscaling(self):

        project_id = "cloud-custodian"

        factory = self.replay_flight_data('gke-cluster-nodepool-set-autoscaling', project_id)

        p = self.load_policy({
            'name': 'gke-cluster-nodepool-set-autoscaling',
            'resource': 'gcp.gke-nodepool',
            'filters': [{
                'type': 'value',
                'key': 'initialNodeCount',
                'value': 3
            }],
            'actions': [{
                'type': 'set-autoscaling',
                'enabled': 'True',
                'minNodeCount': '1',
                'maxNodeCount': '3'
            }],
        }, session_factory=factory)

        resources = p.run()

        self.assertEqual(1, len(resources))

        files_dir = os.path.join(os.path.dirname(__file__),
                                 'data', 'flights', 'gke-cluster-nodepool-set-autoscaling')

        files_paths = [file_path for file_path in os.listdir(files_dir)
                       if file_path.__contains__('setAutoscaling')]

        self.assertEqual(1, len(files_paths))

        for file_path in files_paths:
            with open(os.path.join(files_dir, file_path), 'rt') as file:
                response = json.load(file)
                self.assertEqual('UPDATE_CLUSTER', response['body']['operationType'])

    def test_cluster_node_pools_set_size(self):

        project_id = "cloud-custodian"

        factory = self.replay_flight_data('gke-cluster-nodepool-set-size', project_id)

        p = self.load_policy(
            {
                'name': 'gke-cluster-nodepool-set-size',
                'resource': 'gcp.gke-nodepool',
                'filters': [{
                    'type': 'value',
                    'key': 'initialNodeCount',
                    'value': 2,
                    'op': 'greater-than'
                }],
                'actions': [{
                    'type': 'set-size',
                    'node-count': '3',
                }],
            }, session_factory=factory)

        resources = p.run()

        self.assertEqual(1, len(resources))

        files_dir = os.path.join(os.path.dirname(__file__),
                                 'data', 'flights', 'gke-cluster-nodepool-set-size')

        files_paths = [file_path for file_path in os.listdir(files_dir)
                       if file_path.__contains__('setSize')]

        self.assertEqual(1, len(files_paths))

        for file_path in files_paths:
            with open(os.path.join(files_dir, file_path), 'rt') as file:
                response = json.load(file)
                self.assertEqual('SET_NODE_POOL_SIZE', response['body']['operationType'])

    def test_cluster_node_pools_set_auto_upgrade(self):

        project_id = "cloud-custodian"

        factory = self.replay_flight_data('gke-cluster-nodepool-set-auto-upgrade', project_id)

        p = self.load_policy(
            {
                'name': 'gke-cluster-nodepool-set-auto-upgrade',
                'resource': 'gcp.gke-nodepool',
                'actions': [{
                    'type': 'set-management',
                    'auto-upgrade': 'true',
                }],
            }, session_factory=factory)

        resources = p.run()

        self.assertEqual(1, len(resources))

        files_dir = os.path.join(os.path.dirname(__file__),
                                 'data', 'flights', 'gke-cluster-nodepool-set-auto-upgrade')

        files_paths = [file_path for file_path in os.listdir(files_dir)
                       if file_path.__contains__('setManagement')]

        self.assertEqual(1, len(files_paths))

        for file_path in files_paths:
            with open(os.path.join(files_dir, file_path), 'rt') as file:
                response = json.load(file)
                self.assertEqual("SET_NODE_POOL_MANAGEMENT", response['body']['operationType'])
