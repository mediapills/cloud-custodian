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

from gcp_common import BaseTest, event_data


class MLModelTest(BaseTest):

    def test_models_query(self):
        project_id = 'cloud-custodian'

        session_factory = self.replay_flight_data(
            'ml-models-query', project_id)

        policy = self.load_policy(
            {
                'name': 'ml-models-query',
                'resource': 'gcp.ml-model'
            },
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(len(resources), 1)

    def test_models_get(self):
        project_id = 'cloud-custodian'
        name = 'test_model'

        factory = self.replay_flight_data('ml-model-get', project_id=project_id)
        p = self.load_policy({
            'name': 'ml-model-get',
            'resource': 'gcp.ml-model',
            'mode': {
                'type': 'gcp-audit',
                'methods': ['google.cloud.ml.v1.ModelService.CreateModel']
            }
        }, session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('ml-model-create.json')
        models = exec_mode.run(event, None)
        self.assertIn(name, models[0]['name'])

    def test_models_set(self):
        project_id = 'cloud-custodian'
        description = 'Custom description'

        factory = self.replay_flight_data('ml-model-update-description', project_id)

        base_policy = {
            'name': 'ml-model-update-description',
            'resource': 'gcp.ml-model',
            'filters': [{
                'type': 'value',
                'key': 'name',
                'value': 'projects/cloud-custodian/models/test'
            }]}

        p = self.load_policy(
            dict(base_policy, actions=[{
                'type': 'set',
                'description': description
            }]),
            session_factory=factory)

        resources = p.run()

        self.assertEqual(resources[0]['description'], description)

    def test_model_delete(self):
        project_id = 'cloud-custodian'
        name = 'projects/cloud-custodian/models/test'
        factory = self.replay_flight_data('ml-model-delete', project_id)

        base_policy = {
            'name': 'ml-model-delete',
            'resource': 'gcp.ml-model',
            'filters': [{
                'type': 'value',
                'key': 'name',
                'value': name
            }]}

        p = self.load_policy(
            dict(base_policy, actions=[{
                'type': 'delete'
            }]),
            session_factory=factory)

        resources = p.run()

        self.assertEqual(resources[0]['name'], name)

        client = p.resource_manager.get_client()
        result = client.execute_query(
            'list', {'parent': 'projects/' + project_id})

        self.assertEqual(len(result), 0)

    def test_model_set_iam_policy(self):
        project_id = 'cloud-custodian'
        resource_full_name = 'projects/{}/models/test_model_demo'.format(project_id)
        session_factory = self.replay_flight_data(
            'ml-model-set-iam-policy', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-ml-model',
             'resource': 'gcp.ml-model',
             'filters': [{'type': 'value',
                          'key': 'name',
                          'value': resource_full_name}],
             'actions': [{'type': 'set-iam-policy',
                          'add-bindings':
                              [{'members': ['user:alex.karpitski@gmail.com'],
                                'role': 'roles/ml.modelOwner'}]}]},
            session_factory=session_factory)

        client = policy.resource_manager.get_client()
        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': ['user:c7n.test@gmail.com'],
                           'role': 'roles/ml.modelOwner'}])

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_full_name)

        if self.recording:
            time.sleep(1)

        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': ['user:alex.karpitski@gmail.com',
                                       'user:c7n.test@gmail.com'],
                           'role': 'roles/ml.modelOwner'}])


class MLJobTest(BaseTest):

    def test_jobs_query(self):
        project_id = 'cloud-custodian'

        session_factory = self.replay_flight_data(
            'ml-jobs-query', project_id)

        policy = self.load_policy(
            {
                'name': 'ml-jobs-query',
                'resource': 'gcp.ml-job'
            },
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(len(resources), 1)

    def test_jobs_get(self):
        project_id = 'cloud-custodian'
        name = 'test_job'

        factory = self.replay_flight_data('ml-job-get', project_id=project_id)
        p = self.load_policy({
            'name': 'ml-job-get',
            'resource': 'gcp.ml-job',
            'mode': {
                'type': 'gcp-audit',
                'methods': ['google.cloud.ml.v1.JobService.CreateJob']
            }
        }, session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('ml-job-create.json')
        jobs = exec_mode.run(event, None)
        self.assertIn(name, jobs[0]['jobId'])

    def test_jobs_set(self):
        project_id = 'cloud-custodian'

        factory = self.replay_flight_data('ml-job-set-labels', project_id)

        base_policy = {'name': 'ml-job-set-labels',
                       'resource': 'gcp.ml-job',
                       'filters': [{
                           'type': 'value',
                           'key': 'jobId',
                           'value': 'test_job'
                       }]}

        p = self.load_policy(
            dict(base_policy,
                 actions=[{
                     'type': 'set',
                     'labels': {
                         'version': 'current'
                     }
                 }]),
            session_factory=factory)

        p.run()

        p = self.load_policy(base_policy, session_factory=factory)

        resources = p.run()

        self.assertEqual(resources[0]['labels'], {'version': 'current'})

    def test_jobs_set_iam_policy(self):
        project_id = 'cloud-custodian'
        resource_name = 'test_job'
        resource_full_name = 'projects/{}/jobs/{}'.format(project_id, resource_name)
        session_factory = self.replay_flight_data(
            'ml-job-set-iam-policy', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-ml-job',
             'resource': 'gcp.ml-job',
             'filters': [{'type': 'value',
                          'key': 'jobId',
                          'value': resource_name}],
             'actions': [{'type': 'set-iam-policy',
                          'add-bindings':
                              [{'members': ['user:alex.karpitski@gmail.com'],
                                'role': 'roles/ml.jobOwner'}]}]},
            session_factory=session_factory)

        client = policy.resource_manager.get_client()
        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': ['user:c7n.test@gmail.com'],
                           'role': 'roles/ml.jobOwner'}])

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['jobId'], resource_name)

        if self.recording:
            time.sleep(1)

        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': ['user:alex.karpitski@gmail.com',
                                       'user:c7n.test@gmail.com'],
                           'role': 'roles/ml.jobOwner'}])
