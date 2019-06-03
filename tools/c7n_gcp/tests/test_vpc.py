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


class VpcAccessPolicyTest(BaseTest):

    def test_vpc_access_policy_query(self):
        factory = self.replay_flight_data('vpc-access-policies-query')
        policy = self.load_policy(
            {'name': 'all-vpc-access-policies',
             'resource': 'gcp.vpc-access-policy',
             'query': [{'organization_id': '926683928810'}]
             },
            session_factory=factory)
        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], 'accessPolicies/1016634752304')


class VpcAccessLevelTest(BaseTest):

    def test_vpc_access_level_query(self):
        factory = self.replay_flight_data('vpc-access-levels-query')
        policy = self.load_policy(
            {'name': 'all-vpc-access-levels',
             'resource': 'gcp.vpc-access-level',
             'query': [{'organization_id': '926683928810'}]
             },
            session_factory=factory)
        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'],
                         'accessPolicies/1016634752304/accessLevels/custodian_admin')
        self.assertIn('BY', resources[0]['basic']['conditions'][0]['regions'])


class VpcServicePerimeterTest(BaseTest):

    def test_vpc_access_level_query(self):
        factory = self.replay_flight_data('vpc-service-perimeters-query')
        policy = self.load_policy(
            {'name': 'all-vpc-service-perimeters',
             'resource': 'gcp.vpc-service-perimeter',
             'query': [{'organization_id': '926683928810'}]
             },
            session_factory=factory)
        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'],
                         'accessPolicies/1016634752304/servicePerimeters/custodian_perimeter_core')
        self.assertEqual(len(resources[0]['status']['resources']), 2)
        self.assertEqual(len(resources[0]['status']['accessLevels']), 1)
        self.assertEqual(resources[0]['status']['accessLevels'][0],
                         'accessPolicies/1016634752304/accessLevels/custodian_admin')
