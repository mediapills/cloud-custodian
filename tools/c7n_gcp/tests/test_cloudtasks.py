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


class CloudTasksLocationTest(BaseTest):

    def test_location_query(self):
        project_id = 'cloud-custodian'
        location_name = 'europe-west3'
        resource_name = 'projects/{}/locations/{}'.format(project_id, location_name)
        session_factory = self.replay_flight_data(
            'cloudtasks-location-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'cloudtasks-location-dryrun',
             'resource': 'gcp.cloudtasks-location'},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_name)


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
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], parent_resource_name)

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
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        exec_mode = policy.get_execution_mode()
        event = event_data('cloudtasks-queue-create.json')
        resources = exec_mode.run(event, None)
        self.assertEqual(resources[0]['name'], resource_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], parent_resource_name)


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
