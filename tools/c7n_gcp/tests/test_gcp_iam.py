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

from gcp_common import BaseTest, event_data


class ProjectRoleTest(BaseTest):

    def test_get(self):
        factory = self.replay_flight_data('iam-project-role')
        p = self.load_policy({
            'name': 'role-get',
            'resource': 'gcp.project-role'},
            session_factory=factory)
        resource = p.resource_manager.get_resource(
            {'project_id': 'custodian-1291',
             'role_name': 'projects/custodian-1291/roles/CustomDeveloperRole'})
        self.assertEqual(resource['title'], 'Developer Role')


class ServiceAccountTest(BaseTest):

    def test_get(self):
        factory = self.replay_flight_data('iam-service-account')
        p = self.load_policy({
            'name': 'sa-get',
            'resource': 'gcp.service-account'},
            session_factory=factory)
        resource = p.resource_manager.get_resource(
            {'project_id': 'custodian-1291',
             'email_id': 'devtest@custodian-1291.iam.gserviceaccount.com',
             'unique_id': '110936229421407410679'})
        self.assertEqual(resource['displayName'], 'devtest')


class IAMRoleTest(BaseTest):

    def test_iam_role_query(self):
        project_id = "cloud-custodian"

        session_factory = self.replay_flight_data(
            'ami-role-query', project_id)

        policy = self.load_policy(
            {
                'name': 'ami-role-query',
                'resource': 'gcp.iam-role'
            },
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(len(resources), 2)

    def test_iam_role_get(self):
        project_id = 'cloud-custodian'
        name = "accesscontextmanager.policyAdmin"

        session_factory = self.replay_flight_data(
            'ami-role-query-get', project_id)

        policy = self.load_policy(
            {
                'name': 'ami-role-query-get',
                'resource': 'gcp.iam-role'
            },
            session_factory=session_factory)

        resource = policy.resource_manager.get_resource({
            "name": name,
        })

        self.assertEqual(resource['name'], 'roles/{}'.format(name))


class ServiceAccountKeyTest(BaseTest):

    def test_iam_role_query(self):
        project_id = "test-project-232910"

        session_factory = self.replay_flight_data(
            'ami-service-account-key-query', project_id)

        policy = self.load_policy(
            {
                'name': 'ami-service-account-key-query',
                'resource': 'gcp.service-account-key'
            },
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(len(resources), 1)

    def test_get(self):
        project_id = 'mitrop-custodian'
        key_algorithm = 'KEY_ALG_RSA_2048'
        factory = self.replay_flight_data('aim-service-account-key-get', project_id)
        p = self.load_policy({'name': 'sa-key-get',
                              'resource': 'gcp.service-account-key',
                              # },
                              'mode': {
                                  'type': 'gcp-audit',
                                  'methods': ['google.iam.admin.v1.CreateServiceAccountKey']}
                              },
                             session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('iam-sa-key-create.json')
        resource = exec_mode.run(event, None)
        self.assertEqual(resource[0]['keyAlgorithm'], key_algorithm)
