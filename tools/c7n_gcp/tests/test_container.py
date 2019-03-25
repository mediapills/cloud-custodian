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

#  TODO: do we need to test list action exception


class ContainerClusterLocationTest(BaseTest):

    def test_cluster_location_query(self):
        project_id = "cloud-custodian"

        factory = self.replay_flight_data('container-location-cluster-query', project_id)
        p = self.load_policy(
            {'name': 'all-container-location-cluster',
             'resource': 'gcp.container-location-cluster'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['status'], 'RUNNING')
        self.assertEqual(resources[0]['name'], 'standard-cluster-1')
        self.assertIn(resources[0]['location'], 'us-central1-a')

    def test_cluster_location_get(self):
        project_id = "cloud-custodian"
        name = "standard-cluster-1"
        factory = self.replay_flight_data('container-location-cluster-get', project_id)

        p = self.load_policy(
            {'name': 'one-container-location-cluster',
             'resource': 'gcp.container-location-cluster'},
            session_factory=factory)
        instance = p.resource_manager.get_resource(
            {"project_id": project_id,
             "location": "us-central1-a",
             "cluster": name})

        self.assertEqual(instance['name'], name)
        self.assertEqual(instance['status'], 'RUNNING')
        self.assertIn(instance['location'], 'us-central1-a')


class ContainerZoneTest(BaseTest):

    def test_zone_get(self):
        project_id = "cloud-custodian"
        zone = "us-central1-a"
        factory = self.replay_flight_data('container-zone-get', project_id)

        p = self.load_policy(
            {'name': 'one-container-zone',
             'resource': 'gcp.container-zone'},
            session_factory=factory)
        instance = p.resource_manager.get_resource(
            {"project_id": project_id,
             "zone": zone})

        self.assertIn(instance['defaultClusterVersion'], '1.11.7-gke.4')
        self.assertIn(instance['defaultImageType'], 'COS', )


class ContainerLocationTest(BaseTest):

    def test_location_get(self):
        project_id = "cloud-custodian"
        location = "us-central1-a"
        factory = self.replay_flight_data('container-location-get', project_id)

        p = self.load_policy(
            {'name': 'one-container-location',
             'resource': 'gcp.container-location'},
            session_factory=factory)
        instance = p.resource_manager.get_resource(
            {"project_id": project_id,
             "location": location})

        self.assertIn(instance['defaultClusterVersion'], '1.11.7-gke.4')
        self.assertIn(instance["defaultImageType"], 'COS')
