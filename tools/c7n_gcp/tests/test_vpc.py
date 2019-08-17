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
import time


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

    def test_vpc_access_policy_delete(self):
        organization_id = '926683928810'
        session_factory = self.replay_flight_data('vpc-access-policies-delete')
        base_policy = {'name': 'vpc-access-policies-delete',
                       'resource': 'gcp.vpc-access-policy'}
        policy = self.load_policy(
            dict(base_policy,
                 query=[{'organization_id': organization_id}],
                 filters=[{'parent': 'organizations/926683928810'}],
                 actions=[{'type': 'delete'}]
                 ),
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(1, len(resources))
        self.assertEqual('organizations/926683928810', resources[0]['parent'])

        if self.recording:
            time.sleep(10)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'parent': 'organizations/' + organization_id})
        self.assertIsNone(result.get('accessPolicies'))


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

    def test_vpc_access_level_delete(self):
        organization_id = '926683928810'
        session_factory = self.replay_flight_data('vpc-access-levels-delete')
        base_policy = {'name': 'vpc-access-levels-delete',
                       'resource': 'gcp.vpc-access-level'}
        policy = self.load_policy(
            dict(base_policy,
                 query=[{'organization_id': organization_id}],
                 filters=[{'type': 'value',
                           'key': 'title',
                           'value': 'custodian_admin_2',
                           'op': 'eq'}],
                 actions=[{'type': 'delete'}]),
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(1, len(resources))
        self.assertEqual('accessPolicies/1016634752304/accessLevels/custodian_admin_2',
                         resources[0]['name'])
        self.assertEqual('custodian_admin_2', resources[0]['title'])

        if self.recording:
            time.sleep(10)

        client = policy.resource_manager.get_client()

        result = client.execute_query('list', {'parent': 'accessPolicies/1016634752304'})

        access_levels = result['accessLevels']
        self.assertEqual(2, len(access_levels))
        self.assertEqual('accessPolicies/1016634752304/accessLevels/custodian_admin',
                         access_levels[0]['name'])
        self.assertEqual('accessPolicies/1016634752304/accessLevels/custodian_viewer',
                         access_levels[1]['name'])

    def test_vpc_access_level_patch(self):
        organization_id = '926683928810'
        session_factory = self.replay_flight_data('vpc-access-levels-patch')
        base_policy = {'name': 'vpc-access-levels-patch',
                       'resource': 'gcp.vpc-access-level'}
        policy = self.load_policy(
            dict(base_policy,
                 query=[{'organization_id': organization_id}],
                 filters=[{'type': 'value',
                           'key': 'title',
                           'value': 'custodian_admin',
                           'op': 'eq'}],
                 actions=[{'type': 'set',
                           'description': 'new description',
                           'basic': {
                               'conditions': [{
                                   'regions': [
                                       'BY',
                                       'US',
                                       'RU'
                                   ]}]}
                           }]),
            session_factory=session_factory, validate=True)

        resources = policy.run()
        self.assertEqual(1, len(resources))
        self.assertEqual('accessPolicies/1016634752304/accessLevels/custodian_admin',
                         resources[0]['name'])
        self.assertEqual('custodian_admin', resources[0]['title'])
        self.assertEqual(['BY', 'GB'], resources[0]['basic']['conditions'][0]['regions'])
        self.assertEqual('no description', resources[0]['description'])

        if self.recording:
            time.sleep(10)

        client = policy.resource_manager.get_client()

        result = client.execute_query('list', {'parent': 'accessPolicies/1016634752304'})

        access_levels = result['accessLevels']
        self.assertEqual(3, len(access_levels))
        self.assertEqual('accessPolicies/1016634752304/accessLevels/custodian_admin',
                         access_levels[0]['name'])
        self.assertEqual('custodian_admin', access_levels[0]['title'])
        self.assertEqual('new description', access_levels[0]['description'])
        self.assertEqual(['BY', 'US', 'RU'],
                         access_levels[0]['basic']['conditions'][0]['regions'])
        self.assertEqual('accessPolicies/1016634752304/accessLevels/custodian_viewer',
                         access_levels[1]['name'])
        self.assertEqual('accessPolicies/1016634752304/accessLevels/custodian_admin_2',
                         access_levels[2]['name'])


class VpcServicePerimeterTest(BaseTest):

    def test_vpc_service_perimeter_query(self):
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

    def test_vpc_service_perimeter_delete(self):
        organization_id = '926683928810'
        session_factory = self.replay_flight_data('vpc-service-perimeter-delete')
        base_policy = {'name': 'vpc-service-perimeter-delete',
                       'resource': 'gcp.vpc-service-perimeter'}
        policy = self.load_policy(
            dict(base_policy,
                 query=[{'organization_id': organization_id}],
                 filters=[{'type': 'value',
                           'key': 'status.accessLevels',
                           'value': 'accessPolicies/1016634752304/accessLevels/custodian_viewer',
                           'op': 'contains'}],
                 actions=[{'type': 'delete'}]
                 ),
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(1, len(resources))
        service_perimeter_name_viewer = \
            'accessPolicies/1016634752304/servicePerimeters/custodian_service_perimeter_viewer_0'
        self.assertEqual(service_perimeter_name_viewer, resources[0]['name'])
        self.assertEqual(['projects/359546646409', 'projects/2030697917'],
                         resources[0]['status']['resources'])
        self.assertEqual(['accessPolicies/1016634752304/accessLevels/custodian_viewer',
                          'accessPolicies/1016634752304/accessLevels/custodian_viewer_2'],
                         resources[0]['status']['accessLevels'])
        self.assertEqual(['bigquery.googleapis.com', 'pubsub.googleapis.com'],
                         resources[0]['status']['restrictedServices'])

        if self.recording:
            time.sleep(10)

        client = policy.resource_manager.get_client()

        result = client.execute_query('list', {'parent': 'accessPolicies/1016634752304'})

        service_perimeters = result['servicePerimeters']
        self.assertEqual(1, len(service_perimeters))
        service_perimeter_name_core = \
            'accessPolicies/1016634752304/servicePerimeters/custodian_perimeter_core'
        self.assertEqual(service_perimeter_name_core, service_perimeters[0]['name'])

    def test_vpc_service_perimeter_set(self):
        organization_id = '926683928810'
        service_perimeter_name_viewer = \
            'accessPolicies/1016634752304/servicePerimeters/custodian_service_perimeter_viewer_0'
        service_perimeter_name_core = \
            'accessPolicies/1016634752304/servicePerimeters/custodian_perimeter_core'
        session_factory = self.replay_flight_data('vpc-service-perimeter-patch')
        base_policy = {'name': 'vpc-service-perimeter-patch',
                       'resource': 'gcp.vpc-service-perimeter'}
        policy = self.load_policy(
            dict(base_policy,
                 query=[{'organization_id': organization_id}],
                 filters=[{'type': 'value',
                           'key': 'status.accessLevels',
                           'value': 'accessPolicies/1016634752304/accessLevels/custodian_viewer',
                           'op': 'contains'}],
                 actions=[{'type': 'set',
                           'status': {
                               'resources': [
                                   'projects/custodian-test-project',
                                   'projects/custodian-test-project-3'
                               ],
                               'accessLevels': [
                                   'accessPolicies/1016634752304/accessLevels/custodian_viewer',
                                   'accessPolicies/1016634752304/accessLevels/custodian_viewer_2'
                               ],
                               'restrictedServices': [
                                   'bigquery.googleapis.com',
                                   'pubsub.googleapis.com'
                               ]
                           }
                           }]
                 ),
            session_factory=session_factory, validate=True)

        resources = policy.run()
        self.assertEqual(1, len(resources))
        self.assertEqual(service_perimeter_name_viewer, resources[0]['name'])
        self.assertEqual(['projects/359546646409', 'projects/2030697917'],
                         resources[0]['status']['resources'])
        self.assertEqual(['accessPolicies/1016634752304/accessLevels/custodian_viewer'],
                         resources[0]['status']['accessLevels'])
        self.assertEqual(['bigquery.googleapis.com', 'pubsub.googleapis.com'],
                         resources[0]['status']['restrictedServices'])

        if self.recording:
            time.sleep(10)

        client = policy.resource_manager.get_client()

        result = client.execute_query('list', {'parent': 'accessPolicies/1016634752304'})

        service_perimeters = result['servicePerimeters']
        self.assertEqual(2, len(service_perimeters))
        self.assertEqual(service_perimeter_name_core, service_perimeters[0]['name'])
        self.assertEqual(service_perimeter_name_viewer, service_perimeters[1]['name'])
        self.assertEqual(['accessPolicies/1016634752304/accessLevels/custodian_viewer',
                          'accessPolicies/1016634752304/accessLevels/custodian_viewer_2'],
                         service_perimeters[1]['status']['accessLevels'])
