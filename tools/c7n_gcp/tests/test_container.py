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

from gcp_common import BaseTest


class ContainerLocationTest(BaseTest):

    def test_locations_query(self):
        project_id = "cloud-custodian"

        factory = self.replay_flight_data('container-location-query', project_id)
        p = self.load_policy(
            {'name': 'all-container-location',
             'resource': 'gcp.container-location'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_locations_get(self):
        project_id = "cloud-custodian"
        name = "standard-cluster-1"
        factory = self.replay_flight_data('container-location-get', project_id)

        p = self.load_policy(
            {'name': 'one-container-location',
             'resource': 'gcp.container-location'},
            session_factory=factory)
        instance = p.resource_manager.get_resource(
            {"project_id": project_id,
             "location": "us-central1-a",
             "cluster": name})

        self.assertEqual(instance['name'], name)


class ContainerOperationTest(BaseTest):

    def test_operations_query(self):
        project_id = "mythic-tribute-232915"  # "cloud-custodian"

        factory = self.replay_flight_data('container-operation-query', project_id)
        p = self.load_policy(
            {'name': 'all-container-operation',
             'resource': 'gcp.container-operation'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_operations_get(self):
        project_id = "mythic-tribute-232915"  # "cloud-custodian"
        name = "operation-1554901519839-e2bbf54f"
        factory = self.replay_flight_data('container-operation-get', project_id)

        p = self.load_policy(
            {'name': 'one-container-operation',
             'resource': 'gcp.container-operation'},
            session_factory=factory)
        instance = p.resource_manager.get_resource(
            {"project_id": project_id,
             "location": "us-central1-a",
             "operation": name})

        self.assertEqual(instance['name'], name)
