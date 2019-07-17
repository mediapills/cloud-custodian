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
import re

from gcp_common import BaseTest, event_data
from googleapiclient.errors import HttpError

class CloudIotRegistryTest(BaseTest):

    def test_registry_query(self):
        project_id = 'cloud-custodian'
        resource_id = 'custodian'
        session_factory = self.replay_flight_data(
            'cloudiot-registry-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudiot-registry-dryrun',
             'resource': 'gcp.cloudiot-registry',
             'query':
                 [{'location': 'europe-west1'}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['id'], resource_id)

    def test_registry_get(self):
        project_id = 'cloud-custodian'
        resource_id = 'custodian'
        session_factory = self.replay_flight_data(
            'cloudiot-registry-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudiot-registry-audit',
             'resource': 'gcp.cloudiot-registry',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': ['google.cloud.iot.v1.DeviceManager.CreateDeviceRegistry']
             }},
            session_factory=session_factory)

        exec_mode = policy.get_execution_mode()
        event = event_data('cloudiot-registry-create.json')
        resources = exec_mode.run(event, None)
        self.assertEqual(resources[0]['id'], resource_id)

    def test_registry_delete(self):
        project_id = 'cloud-custodian-190204'
        location_id = 'europe-west1'
        resource_id = 'registry-to-delete'
        self_link = 'projects/%s/locations/%s/registries/%s' % (project_id, location_id, resource_id)
        session_factory = self.replay_flight_data(
            'cloudiot-registry-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudiot-registry-audit',
             'resource': 'gcp.cloudiot-registry',
             'actions': [{'type': 'delete'}],
             'query': [{'location': location_id}],
             'filters': [{
                 'type': 'value',
                 'key': 'id',
                 'value': resource_id
             }]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['id'], resource_id)

        client = policy.resource_manager.get_client()
        try:
            result = client.execute_query(
                'get', {'name': self_link})
            self.fail('found deleted resource: %s' % result)
        except HttpError as e:
            self.assertTrue(re.match(".*A registry with the name '.+?' doesn't exist.*", str(e)))


class CloudIotDeviceTest(BaseTest):

    def test_device_query(self):
        project_id = 'cloud-custodian'
        resource_id = 'custodian-device'
        parent_resource_id = 'custodian'
        session_factory = self.replay_flight_data(
            'cloudiot-device-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudiot-device-dryrun',
             'resource': 'gcp.cloudiot-device',
             'query':
                 [{'location': 'europe-west1'}]},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(resources[0]['id'], resource_id)
        self.assertEqual(resources[0][parent_annotation_key]['id'], parent_resource_id)

    def test_device_get(self):
        project_id = 'cloud-custodian'
        resource_id = 'custodian-device'
        parent_resource_id = 'custodian'
        session_factory = self.replay_flight_data(
            'cloudiot-device-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudiot-device-audit',
             'resource': 'gcp.cloudiot-device',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': ['google.cloud.iot.v1.DeviceManager.CreateDevice']
             }},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        exec_mode = policy.get_execution_mode()
        event = event_data('cloudiot-device-create.json')
        resources = exec_mode.run(event, None)
        self.assertEqual(resources[0]['id'], resource_id)
        self.assertEqual(resources[0][parent_annotation_key]['id'], parent_resource_id)
