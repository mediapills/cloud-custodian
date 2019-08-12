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

import time

from gcp_common import BaseTest


class OrganizationTest(BaseTest):

    def test_organization_query(self):
        organization_name = 'organizations/851339424791'
        session_factory = self.replay_flight_data('organization-query')

        policy = self.load_policy(
            {'name': 'gcp-organization-dryrun',
             'resource': 'gcp.organization'},
            session_factory=session_factory)

        organization_resources = policy.run()
        self.assertEqual(organization_resources[0]['name'], organization_name)


class FolderTest(BaseTest):

    def test_folder_query(self):
        resource_name = 'folders/112838955399'
        parent = 'organizations/926683928810'
        session_factory = self.replay_flight_data('folder-query')

        policy = self.load_policy(
            {'name': 'gcp-folder-dryrun',
             'resource': 'gcp.folder',
             'query':
                 [{'parent': parent}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0]['parent'], parent)


class ProjectTest(BaseTest):

    def test_project_set_iam_policy(self):
        resource_full_name = 'cloud-custodian-190204'
        session_factory = self.record_flight_data(
            'project-set-iam-policy')

        policy = self.load_policy(
            {'name': 'gcp-project-set-iam-policy',
             'resource': 'gcp.project',
             'filters': [{'type': 'value',
                          'key': 'name',
                          'value': resource_full_name}],
             'actions': [{'type': 'set-iam-policy',
                          'remove-bindings':
                              [{'members': ['user:alex.karpitski@gmail.com'],
                                'role': 'roles/owner'}]}]},
            session_factory=session_factory)

        client = policy.resource_manager.get_client()
        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name,
                                                                'body': {}})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': ['serviceAccount:custodian-five@cloud-custodian-190204.iam.gserviceaccount.com',
                                       'user:alex.karpitski@gmail.com'],
                           'role': 'roles/owner'}])

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_full_name)

        if self.recording:
            time.sleep(1)

        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name,
                                                                'body': {}})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': [
                             'serviceAccount:custodian-five@cloud-custodian-190204.iam.gserviceaccount.com'],
                           'role': 'roles/owner'}])
