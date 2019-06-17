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
import time

from gcp_common import BaseTest, event_data
from googleapiclient.errors import HttpError


class InstanceTest(BaseTest):

    def test_instance_query(self):
        factory = self.replay_flight_data('instance-query')
        p = self.load_policy(
            {'name': 'all-instances',
             'resource': 'gcp.instance'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 4)

    def test_instance_get(self):
        factory = self.replay_flight_data('instance-get')
        p = self.load_policy(
            {'name': 'one-instance',
             'resource': 'gcp.instance'},
            session_factory=factory)
        instance = p.resource_manager.get_resource(
            {"instance_id": "2966820606951926687",
             "project_id": "custodian-1291",
             "resourceName": "projects/custodian-1291/zones/us-central1-b/instances/c7n-jenkins",
             "zone": "us-central1-b"})
        self.assertEqual(instance['status'], 'RUNNING')

    def test_stop_instance(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('instance-stop', project_id=project_id)
        p = self.load_policy(
            {'name': 'istop',
             'resource': 'gcp.instance',
             'filters': [{'name': 'instance-1'}, {'status': 'RUNNING'}],
             'actions': ['stop']},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

        client = p.resource_manager.get_client()
        result = client.execute_query(
            'list', {'project': project_id,
                     'filter': 'name = instance-1',
                     'zone': resources[0]['zone'].rsplit('/', 1)[-1]})
        self.assertEqual(result['items'][0]['status'], 'STOPPING')

    def test_start_instance(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('instance-start', project_id=project_id)
        p = self.load_policy(
            {'name': 'istart',
             'resource': 'gcp.instance',
             'filters': [{'tag:env': 'dev'}, {'status': 'TERMINATED'}],
             'actions': ['start']},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

        if self.recording:
            time.sleep(3)

        client = p.resource_manager.get_client()
        result = client.execute_query(
            'list', {'project': project_id,
                     'filter': 'labels.env=dev',
                     'zone': resources[0]['zone'].rsplit('/', 1)[-1]})
        self.assertEqual(result['items'][0]['status'], 'PROVISIONING')

    def test_delete_instance(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('instance-terminate', project_id=project_id)
        p = self.load_policy(
            {'name': 'iterm',
             'resource': 'gcp.instance',
             'filters': [{'name': 'instance-1'}],
             'actions': ['delete']},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        if self.recording:
            time.sleep(1)
        client = p.resource_manager.get_client()
        result = client.execute_query(
            'list', {'project': project_id,
                     'filter': 'name = instance-1',
                     'zone': resources[0]['zone'].rsplit('/', 1)[-1]})
        self.assertEqual(result['items'][0]['status'], 'STOPPING')


class DiskTest(BaseTest):

    def test_disk_query(self):
        factory = self.replay_flight_data('disk-query')
        p = self.load_policy(
            {'name': 'all-disks',
             'resource': 'gcp.disk'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 6)


class SnapshotTest(BaseTest):

    def test_snapshot_query(self):
        factory = self.replay_flight_data(
            'snapshot-query', project_id='cloud-custodian')
        p = self.load_policy(
            {'name': 'all-disks',
             'resource': 'gcp.snapshot'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_snapshot_delete(self):
        factory = self.replay_flight_data(
            'snapshot-delete', project_id='cloud-custodian')
        p = self.load_policy(
            {'name': 'all-disks',
             'resource': 'gcp.snapshot',
             'filters': [
                 {'name': 'snapshot-1'}],
             'actions': ['delete']},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)


class ImageTest(BaseTest):

    def test_image_query(self):
        factory = self.replay_flight_data(
            'image-query', project_id='cloud-custodian')
        p = self.load_policy(
            {'name': 'all-images',
             'resource': 'gcp.image'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_image_delete(self):
        factory = self.replay_flight_data(
            'image-delete', project_id='cloud-custodian')
        p = self.load_policy(
            {'name': 'all-images',
             'resource': 'gcp.image',
             'filters': [
                 {'name': 'image-1'}],
             'actions': ['delete']},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)


class GceNodeGroupTest(BaseTest):

    def test_node_group_query(self):
        resource_id = 'custodian-sole-tenant'
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data(
            'gce-node-group-query', project_id=project_id)
        p = self.load_policy(
            {'name': 'gcp-gce-node-group-dryrun',
             'resource': 'gcp.gce-node-group'},
            session_factory=factory)

        resources = p.run()
        self.assertEqual(resources[0]['name'], resource_id)

    def test_node_group_get(self):
        resource_id = 'custodian-sole-tenant'
        session_factory = self.replay_flight_data('gce-node-group-get')

        policy = self.load_policy(
            {'name': 'gcp-gce-node-group-audit',
             'resource': 'gcp.gce-node-group',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': ['v1.compute.nodeGroups.insert']
             }},
            session_factory=session_factory)

        exec_mode = policy.get_execution_mode()
        event = event_data('gce-node-group-create.json')
        resources = exec_mode.run(event, None)

        self.assertEqual(resources[0]['name'], resource_id)

    def test_node_group_delete(self):
        project_id = 'epm-gcp-msq-stage'
        zone_id = 'us-central1-f'
        resource_id = 'custodian-sole-tenant'
        resource_full_name = 'projects/%s/zones/%s/nodeGroups/%s'\
                             % (project_id, zone_id, resource_id)
        session_factory = self.replay_flight_data(
            'gce-node-group-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-gce-node-group-delete',
             'resource': 'gcp.gce-node-group',
             'filters': [{
                 'type': 'value',
                 'key': 'name',
                 'value': resource_id
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_id)

        client = policy.resource_manager.get_client()
        try:
            result = client.execute_query(
                'get', {'project': project_id,
                        'zone': zone_id,
                        'nodeGroup': resource_id})
            self.fail('found deleted resource: %s' % result)
        except HttpError as e:
            self.assertTrue(re.match(".*The resource '%s' was not found.*" %
                                     resource_full_name, str(e)))

    def test_node_group_set_size_increase_valid(self):
        self._test_node_group_set_size_valid(1, 2, 'increase-size')

    def test_node_group_set_size_increase_target_not_greater_than_current_error(self):
        self._test_node_group_set_size_error(
            1, 1, 'increase-size', 'error-target-not-greater-than-current', ValueError,
            'Target node group size (1) must be greater than the current (1)')

    def test_node_group_set_size_decrease_valid(self):
        self._test_node_group_set_size_valid(2, 1, 'decrease-size')

    def test_node_group_set_size_decrease_target_not_smaller_than_current_error(self):
        self._test_node_group_set_size_error(
            2, 2, 'decrease-size', 'error-target-not-smaller-than-current', ValueError,
            'Target node group size (2) must be smaller than the current (2)')

    def _test_node_group_set_size_valid(self, current_size, target_size, action_type):
        project_id, zone_id, resource_id, policy, resources =\
            self._test_node_group_set_size_base(current_size, target_size, action_type, 'valid')
        self.assertEqual(resources[0]['name'], resource_id)

        if self.recording:
            time.sleep(15)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'get', {'project': project_id,
                    'zone': zone_id,
                    'nodeGroup': resource_id})
        self.assertEqual(result['size'], target_size)

    def _test_node_group_set_size_error(self, current_size, target_size, action_type, flight_id,
                                        error_class, error_message):
        try:
            self._test_node_group_set_size_base(current_size, target_size, action_type, flight_id)
        except error_class as e:
            self.assertEqual(error_message, str(e))

    def _test_node_group_set_size_base(self, current_size, target_size, action_type, flight_id):
        project_id = 'epm-gcp-msq-stage'
        zone_id = 'us-central1-f'
        resource_id = 'custodian-sole-tenant'
        session_factory = self.replay_flight_data(
            'gce-node-group-%s-%s' % (action_type, flight_id), project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-gce-node-group-set-size',
             'resource': 'gcp.gce-node-group',
             'filters': [{
                 'type': 'value',
                 'key': 'size',
                 'value': current_size
             }],
             'actions': [{'type': action_type,
                          'target-size': target_size}]},
            session_factory=session_factory)

        resources = policy.run()
        return project_id, zone_id, resource_id, policy, resources
