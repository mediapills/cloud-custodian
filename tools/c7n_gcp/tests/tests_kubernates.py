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

import time
from gcp_common import BaseTest
from googleapiclient.errors import HttpError


class KubernatesTest(BaseTest):

    def test_locations_query(self):
        project_id = "mythic-tribute-232915"

        factory = self.replay_flight_data('kubernetes-project-location-query', project_id)
        p = self.load_policy(
            {'name': 'all-kubernetes-project-location',
             'resource': 'gcp.kubernetes-project-location'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['status'], 'RUNNING')
        self.assertEqual(resources[0]['name'], 'standard-cluster-1')
        self.assertIn('us-central1-a', resources[0]['locations'])

    def test_locations_get(self):
        project_id = "mythic-tribute-232915"
        name = "standard-cluster-1"
        factory = self.replay_flight_data('kubernetes-project-location-get', project_id)

        p = self.load_policy(
            {'name': 'one-kubernetes-project-location',
             'resource': 'gcp.kubernetes-project-location'},
            session_factory=factory)
        instance = p.resource_manager.get_resource(
            {"project_id": project_id,
             "location": "us-central1-a",
             "cluster": name})

        self.assertEqual(instance['name'], name)
        self.assertEqual(instance['status'], 'RUNNING')
        self.assertIn('us-central1-a', instance['locations'])

