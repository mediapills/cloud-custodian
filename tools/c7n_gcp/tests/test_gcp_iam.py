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
from time import sleep

from google.auth.exceptions import RefreshError

from gcp_common import BaseTest, event_data


class ProjectRoleTest(BaseTest):

    def test_get(self):
        factory = self.replay_flight_data('iam-project-role')

        p = self.load_policy({
            'name': 'role-get',
            'resource': 'gcp.project-role',
            'mode': {
                'type': 'gcp-audit',
                'methods': ['google.iam.admin.v1.CreateRole']}},
            session_factory=factory)

        exec_mode = p.get_execution_mode()
        event = event_data('iam-role-create.json')
        roles = exec_mode.run(event, None)

        self.assertEqual(len(roles), 1)
        self.assertEqual(roles[0]['name'], 'projects/mythic-tribute-232915/roles/CustomRole1')

    def test_role_set(self):
        project_id = 'cloud-custodian'
        name = "projects/cloud-custodian/roles/CustomRole"
        session_factory = self.replay_flight_data(
            'iam-project-role-update-title', project_id=project_id)

        base_policy = {'name': 'gcp-iam-project-role-update-title',
                       'resource': 'gcp.project-role',
                       'filters': [{
                           'type': 'value',
                           'key': 'name',
                           'value': name
                       }]}

        policy = self.load_policy(
            dict(base_policy,
                 actions=[{
                     'type': 'set',
                     'title': 'CustomRole1'
                 }]),
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['title'], 'CustomRole')

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'parent': 'projects/cloud-custodian'})

        self.assertEqual(result['roles'][0]['title'], 'CustomRole1')

    def test_role_delete(self):
        project_id = 'cloud-custodian'
        name = "projects/cloud-custodian/roles/CustomRole"
        session_factory = self.replay_flight_data(
            'iam-project-role-delete', project_id=project_id)

        base_policy = {'name': 'gcp-iam-project-role-delete',
                       'resource': 'gcp.project-role'}

        policy = self.load_policy(
            dict(base_policy,
                 filters=[{
                           'type': 'value',
                           'key': 'name',
                           'value': name
                       }],
                 actions=[{'type': 'delete'}]),
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'parent': 'projects/cloud-custodian'})

        self.assertNotIn('roles', result)


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

    def test_service_account_delete(self):
        project_id = 'cloud-custodian'
        name = "projects/cloud-custodian/serviceAccounts/" +\
               "qwwww-235@cloud-custodian.iam.gserviceaccount.com"

        session_factory = self.replay_flight_data(
            'iam-project-service-account-delete', project_id=project_id)

        base_policy = {'name': 'gcp-iam-project-service-account-delete',
                       'resource': 'gcp.service-account'}

        policy = self.load_policy(
            dict(base_policy,
                 filters=[{
                           'type': 'value',
                           'key': 'name',
                           'value': name
                       }],
                 actions=[{'type': 'delete'}]),
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'name': 'projects/cloud-custodian'})

        self.assertNotIn(name, [resource['name'] for resource in result['accounts']])

    def test_service_account_disable(self):
        project_id = 'cloud-custodian'
        name = "projects/cloud-custodian/serviceAccounts/" +\
               "dddddddd@cloud-custodian.iam.gserviceaccount.com"

        session_factory = self.replay_flight_data(
            'iam-project-service-account-disable', project_id=project_id)

        base_policy = {'name': 'gcp-iam-project-service-account-disable',
                       'resource': 'gcp.service-account'}

        policy = self.load_policy(
            dict(base_policy,
                 filters=[{
                           'type': 'value',
                           'key': 'name',
                           'value': name
                       }],
                 actions=[{'type': 'disable'}]),
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'name': 'projects/cloud-custodian'})

        self.assertTrue(result['accounts'][0]['disabled'])

    def test_service_account_enable(self):
        project_id = 'cloud-custodian'
        name = "projects/cloud-custodian/serviceAccounts/" +\
               "dddddddd@cloud-custodian.iam.gserviceaccount.com"

        session_factory = self.replay_flight_data(
            'iam-project-service-account-enable', project_id=project_id)

        base_policy = {'name': 'gcp-iam-project-service-account-enable',
                       'resource': 'gcp.service-account'}

        policy = self.load_policy(
            dict(base_policy,
                 filters=[{
                           'type': 'value',
                           'key': 'name',
                           'value': name
                       }],
                 actions=[{'type': 'enable'}]),
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'name': 'projects/cloud-custodian'})

        self.assertNotIn('disabled', result['accounts'][0])

    def test_service_account_set(self):
        project_id = 'cloud-custodian'
        name = "projects/cloud-custodian/serviceAccounts/" +\
               "dddddddd@cloud-custodian.iam.gserviceaccount.com"
        session_factory = self.replay_flight_data(
            'iam-service-account-set', project_id=project_id)

        base_policy = {'name': 'iam-service-account-set',
                       'resource': 'gcp.service-account',
                       'filters': [{
                           'type': 'value',
                           'key': 'name',
                           'value': name
                       }]}

        policy = self.load_policy(
            dict(base_policy,
                 actions=[{
                     'type': 'set',
                     'display_name': 'test-name'
                 }]),
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['displayName'], 'name')

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'name': 'projects/cloud-custodian'})

        self.assertEqual(result['accounts'][0]['displayName'], 'name')


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
