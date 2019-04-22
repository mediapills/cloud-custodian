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

from gcp_common import BaseTest, event_data


class KmsLocationTest(BaseTest):
    def test_kms_location_query(self):
        project_id = 'cloud-custodian'
        location_name = 'us-west2'
        resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        session_factory = self.replay_flight_data('kms-location-query', project_id=project_id)

        policy = {
            'name': 'all-kms-locations',
            'resource': 'gcp.kms-location'
        }

        policy = self.load_policy(
            policy,
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[24]['name'], resource_name)

    def test_kms_location_get(self):
        project_id = 'cloud-custodian'
        location_name = 'asia'
        session_factory = self.replay_flight_data('kms-location-get', project_id=project_id)

        policy = {
            'name': 'one-kms-location',
            'resource': 'gcp.kms-location'
        }

        policy = self.load_policy(
            policy,
            session_factory=session_factory)

        location = policy.resource_manager.get_resource(
            {'project_id': project_id,
             'location': location_name})

        self.assertEqual(
            location['labels']['cloud.googleapis.com/location'],
            location_name
        )


class KmsKeyRingTest(BaseTest):
    def test_kms_keyring_query(self):
        project_id = 'cloud-custodian'
        location_name = 'us-central1'
        keyring_name = 'cloud-custodian'
        parent_resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        resource_name = '{}/keyRings/{}'.format(parent_resource_name, keyring_name)
        session_factory = self.replay_flight_data('kms-keyring-query', project_id=project_id)

        filter_parent_annotation_key = 'c7n:kms-location'
        policy = self.load_policy(
            {'name': 'gcp-kms-keyring-dryrun',
             'resource': 'gcp.kms-keyring',
             'filters': [{
                 'type': 'value',
                 'key': '\"{}\".name'.format(filter_parent_annotation_key),
                 'op': 'regex',
                 'value': parent_resource_name
             }]},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()
        # If fails there, policies using filters for the resource
        # need to be updated since the key has been changed.
        self.assertEqual(parent_annotation_key, filter_parent_annotation_key)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], parent_resource_name)

    def test_kms_keyring_get(self):
        project_id = 'cloud-custodian'
        location_name = 'us-central1'
        keyring_name = 'cloud-custodian'
        parent_resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        resource_name = '{}/keyRings/{}'.format(parent_resource_name, keyring_name)
        session_factory = self.replay_flight_data('kms-keyring-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-kms-keyring-dryrun',
             'resource': 'gcp.kms-keyring',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': ['CreateKeyRing']
             }},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        exec_mode = policy.get_execution_mode()
        event = event_data('kms-keyring-create.json')
        resources = exec_mode.run(event, None)

        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], parent_resource_name)
