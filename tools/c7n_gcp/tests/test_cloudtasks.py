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

from time import sleep

from gcp_common import BaseTest, event_data
from googleapiclient.errors import HttpError


class CloudTasksQueueTest(BaseTest):

    def test_queue_query(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'custodian-queue'
        parent_resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        resource_name = '{}/queues/{}'.format(parent_resource_name, queue_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-queue-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'cloudtasks-queue-dryrun',
             'resource': 'gcp.cloudtasks-queue'},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_name)

    def test_queue_get(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'custodian-queue-1'
        parent_resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        resource_name = '{}/queues/{}'.format(parent_resource_name, queue_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-queue-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-queue-audit',
             'resource': 'gcp.cloudtasks-queue',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': ['google.cloud.tasks.v2.CloudTasks.CreateQueue']
             }},
            session_factory=session_factory)

        exec_mode = policy.get_execution_mode()
        event = event_data('cloudtasks-queue-create.json')
        resources = exec_mode.run(event, None)
        self.assertEqual(resources[0]['name'], resource_name)

    def test_queue_delete(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'target-queue'
        parent_resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        resource_name = '{}/queues/{}'.format(parent_resource_name, queue_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-queue-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-queue-delete',
             'resource': 'gcp.cloudtasks-queue',
             'filters': [{
                 'type': 'value',
                 'key': 'name',
                 'value': resource_name
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        try:
            result = client.execute_query('get', {'name': resource_name})
            self.fail('found deleted resource: %s' % result)
        except HttpError as e:
            self.assertTrue('Queue does not exist. If you just created the queue, '
                            'wait at least a minute for the queue to initialize.' in str(e))

    def test_queue_set(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'target-queue'
        parent_resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        resource_name = '{}/queues/{}'.format(parent_resource_name, queue_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-queue-set', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-queue-set',
             'resource': 'gcp.cloudtasks-queue',
             'filters': [{
                 'type': 'value',
                 'key': 'name',
                 'value': resource_name
             }],
             'actions': [{'type': 'set',
                          'rate-limits': {
                              'max-concurrent-dispatches': 2,
                              'max-dispatches-per-second': 3
                          },
                          'retry-config': {
                              'max-attempts': 4,
                              'max-backoff': 8,
                              'max-doublings': 6,
                              'max-retry-duration': 7,
                              'min-backoff': 5
                          }}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        resource = client.execute_query('get', {'name': resource_name})
        self.assertEqual(resource['rateLimits']['maxConcurrentDispatches'], 2)
        self.assertEqual(resource['rateLimits']['maxDispatchesPerSecond'], 3)
        self.assertEqual(resource['retryConfig']['maxAttempts'], 4)
        self.assertEqual(resource['retryConfig']['maxBackoff'], '8s')
        self.assertEqual(resource['retryConfig']['maxDoublings'], 6)
        self.assertEqual(resource['retryConfig']['maxRetryDuration'], '7s')
        self.assertEqual(resource['retryConfig']['minBackoff'], '5s')

    def test_queue_set_min_backoff_greater_than_max_backoff(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'target-queue'
        parent_resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        resource_name = '{}/queues/{}'.format(parent_resource_name, queue_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-queue-set-min-backoff-greater-than-max-backoff', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-queue-set',
             'resource': 'gcp.cloudtasks-queue',
             'filters': [{
                 'type': 'value',
                 'key': 'name',
                 'value': resource_name
             }],
             'actions': [{'type': 'set',
                          'retry-config': {
                              'max-backoff': 5,
                              'min-backoff': 8
                          }}]},
            session_factory=session_factory)

        try:
            policy.run()
            self.fail('Should have raised an error.')
        except ValueError as e:
            self.assertEqual('RetryConfig.minBackoff (8s) must be less than or equal to '
                             'RetryConfig.maxBackoff (5s)', str(e))

    def test_set_best_available_value(self):
        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-queue-set',
             'resource': 'gcp.cloudtasks-queue',
             'actions': [{
                 'type': 'set'
             }]})
        test_method = policy.resource_manager.actions[0]._set_best_available_value
        data_key = 'key-string'
        r_key = 'keyString'

        destination_params = {}
        test_method(destination_params, {data_key: 1}, {r_key: 2}, data_key, r_key)
        self.assertEqual(destination_params, {r_key: 1})

        destination_params = {}
        test_method(destination_params, {}, {r_key: 2}, data_key, r_key)
        self.assertEqual(destination_params, {r_key: 2})

        destination_params = {}
        test_method(destination_params, {}, {}, data_key, r_key)
        self.assertEqual(destination_params, {})

        destination_params = {}
        test_method(destination_params, {data_key: 1}, {r_key: '2s'}, data_key, r_key, True)
        self.assertEqual(destination_params, {r_key: '1s'})

        destination_params = {}
        test_method(destination_params, {}, {r_key: '2s'}, data_key, r_key, True)
        self.assertEqual(destination_params, {r_key: '2s'})

    def test_extract_seconds(self):
        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-queue-set',
             'resource': 'gcp.cloudtasks-queue',
             'actions': [{
                 'type': 'set'
             }]})
        test_method = policy.resource_manager.actions[0]._extract_seconds

        self.assertEqual(test_method('1s'), 1.0)

        self.assertEqual(test_method('0.100s'), 0.1)

        try:
            test_method('1')
        except ValueError as e:
            self.assertEqual('A \'%fs\'-formatted string expected (actual - \'1\')', str(e))


class CloudTaskTest(BaseTest):

    def test_task_query(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'custodian-queue'
        task_name = '8298647093923281163'
        parent_resource_name = 'projects/{}/locations/{}/queues/{}'.format(
            project_id, location_name, queue_name)
        resource_name = '{}/tasks/{}'.format(parent_resource_name, task_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-task-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'cloudtasks-task-dryrun',
             'resource': 'gcp.cloudtasks-task'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], parent_resource_name)

    def test_task_get(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'custodian-queue'
        task_name = '8298647093923281163'
        parent_resource_name = 'projects/{}/locations/{}/queues/{}'.format(
            project_id, location_name, queue_name)
        resource_name = '{}/tasks/{}'.format(parent_resource_name, task_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-task-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-task-audit',
             'resource': 'gcp.cloudtasks-task',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': ['google.cloud.tasks.v2.CloudTasks.RunTask']
             }},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        exec_mode = policy.get_execution_mode()
        event = event_data('cloudtasks-task-run.json')
        resources = exec_mode.run(event, None)
        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], parent_resource_name)

    def test_task_delete(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        queue_name = 'primary-queue'
        task_name = 'task-to-delete'
        parent_resource_name = 'projects/{}/locations/{}/queues/{}'.format(
            project_id, location_name, queue_name)
        resource_name = '{}/tasks/{}'.format(parent_resource_name, task_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-task-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-cloudtasks-task-delete',
             'resource': 'gcp.cloudtasks-task',
             'filters': [{
                 'type': 'value',
                 'key': 'name',
                 'value': resource_name
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], parent_resource_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        try:
            result = client.execute_query('get', {'name': resource_name})
            self.fail('found deleted resource: %s' % result)
        except HttpError as e:
            self.assertTrue('The task no longer exists, though a task '
                            'with this name existed recently.' in str(e))
