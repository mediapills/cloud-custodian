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
from time import sleep

from googleapiclient.errors import HttpError


class PubSubTopicTest(BaseTest):

    def test_pubsub_topic_query(self):
        project_id = 'cloud-custodian'
        pubsub_topic_name = 'projects/cloud-custodian/topics/custodian'
        session_factory = self.replay_flight_data(
            'pubsub-topic-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-topic-dryrun',
             'resource': 'gcp.pubsub-topic'},
            session_factory=session_factory)

        pubsub_topic_resources = policy.run()
        self.assertEqual(pubsub_topic_resources[0]['name'], pubsub_topic_name)

    def test_pubsub_topic_get(self):
        project_id = 'cloud-custodian'
        pubsub_topic_name = 'projects/cloud-custodian/topics/custodian'
        session_factory = self.replay_flight_data(
            'pubsub-topic-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-topic-dryrun',
             'resource': 'gcp.pubsub-topic'},
            session_factory=session_factory)

        pubsub_topic_resource = policy.resource_manager.get_resource(
            {'project_id': project_id, 'topic_id': pubsub_topic_name})
        self.assertEqual(pubsub_topic_resource['name'], pubsub_topic_name)

    def test_pubsub_topic_delete(self):
        project_id = 'cloud-custodian'
        resource_name = 'projects/%s/topics/topic-to-delete' % project_id
        session_factory = self.replay_flight_data(
            'pubsub-topic-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-topic-delete',
             'resource': 'gcp.pubsub-topic',
             'filters': [{'type': 'value',
                          'key': 'name',
                          'value': resource_name}],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        result = policy.run()
        self.assertEqual(result[0]['name'], resource_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        try:
            result = client.execute_query(
                'get', {'topic': resource_name})
            self.fail('found deleted resource: %s' % result)
        except HttpError as e:
            self.assertIn("Resource not found", str(e))

    def test_pubsub_topic_set_iam_policy(self):
        project_id = 'cloud-custodian'
        resource_full_name = 'projects/{}/topics/custodian-topic'.format(project_id)
        session_factory = self.replay_flight_data(
            'pubsub-topic-set-iam-policy', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-topic-set-iam-policy',
             'resource': 'gcp.pubsub-topic',
             'filters': [{'type': 'value',
                          'key': 'name',
                          'value': resource_full_name}],
             'actions': [{'type': 'set-iam-policy',
                          'add-bindings':
                              [{'members': ['user:alex.karpitski@gmail.com'],
                                'role': 'roles/owner'}]}]},
            session_factory=session_factory)

        client = policy.resource_manager.get_client()
        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertNotIn('bindings', actual_bindings)

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_full_name)

        if self.recording:
            sleep(1)

        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': ['user:alex.karpitski@gmail.com'],
                           'role': 'roles/owner'}])


class PubSubSubscriptionTest(BaseTest):

    def test_pubsub_subscription_query(self):
        project_id = 'cloud-custodian'
        pubsub_subscription_name = 'projects/cloud-custodian/subscriptions/custodian'
        session_factory = self.replay_flight_data(
            'pubsub-subscription-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-subscription-dryrun',
             'resource': 'gcp.pubsub-subscription'},
            session_factory=session_factory)

        pubsub_subscription_resources = policy.run()
        self.assertEqual(pubsub_subscription_resources[0]['name'], pubsub_subscription_name)

    def test_pubsub_subscription_get(self):
        project_id = 'cloud-custodian'
        subscription_name = 'custodian'
        resource_name = 'projects/{}/subscriptions/{}'.format(project_id, subscription_name)
        session_factory = self.replay_flight_data(
            'pubsub-subscription-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-subscription-audit',
             'resource': 'gcp.pubsub-subscription',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': ['google.pubsub.v1.Subscriber.CreateSubscription']
             }},
            session_factory=session_factory)

        exec_mode = policy.get_execution_mode()
        event = event_data('pubsub-subscription-create.json')
        resources = exec_mode.run(event, None)
        self.assertEqual(resources[0]['name'], resource_name)

    def test_pubsub_subscription_delete(self):
        project_id = 'cloud-custodian'
        resource_name = 'projects/%s/subscriptions/subscription-to-delete' % project_id
        session_factory = self.replay_flight_data(
            'pubsub-subscription-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-subscription-delete',
             'resource': 'gcp.pubsub-subscription',
             'filters': [{'type': 'value',
                          'key': 'name',
                          'value': resource_name}],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        try:
            result = client.execute_query(
                'get', {'subscription': resource_name})
            self.fail('found deleted resource: %s' % result)
        except HttpError as e:
            self.assertIn("Resource not found", str(e))

    def test_pubsub_subscription_set(self):
        project_id = 'cloud-custodian'
        resource_name = 'projects/%s/subscriptions/subscription-to-update' % project_id
        session_factory = self.replay_flight_data(
            'pubsub-subscription-set', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-subscription-set',
             'resource': 'gcp.pubsub-subscription',
             'filters': [{
                 'type': 'value',
                 'key': 'name',
                 'value': resource_name
             }],
             'actions': [{
                 'type': 'set',
                 'expiration-policy-ttl': {
                     'days': 10
                 },
                 'message-retention-duration': {
                     'days': 1,
                     'hours': 2,
                     'minutes': 3
                 }
             }]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query('get', {'subscription': resource_name})
        self.assertEqual(result['name'], resource_name)
        self.assertEqual(result['expirationPolicy']['ttl'], '864000s')
        self.assertEqual(result['messageRetentionDuration'], '93780s')

    def test_pubsub_subscription_set_iam_policy(self):
        project_id = 'cloud-custodian'
        resource_full_name = 'projects/{}/subscriptions/subscription'.format(project_id)
        session_factory = self.replay_flight_data(
            'pubsub-subscription-set-iam-policy', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-subscription-set-iam-policy',
             'resource': 'gcp.pubsub-subscription',
             'filters': [{'type': 'value',
                          'key': 'name',
                          'value': resource_full_name}],
             'actions': [{'type': 'set-iam-policy',
                          'add-bindings':
                              [{'members': ['user:alex.karpitski@gmail.com'],
                                'role': 'roles/owner'}]}]},
            session_factory=session_factory)

        client = policy.resource_manager.get_client()
        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertNotIn('bindings', actual_bindings)

        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], resource_full_name)

        if self.recording:
            sleep(1)

        actual_bindings = client.execute_query('getIamPolicy', {'resource': resource_full_name})
        self.assertEqual(actual_bindings['bindings'],
                         [{'members': ['user:alex.karpitski@gmail.com'],
                           'role': 'roles/owner'}])


class PubSubSnapshotTest(BaseTest):

    def test_pubsub_snapshot_query(self):
        project_id = 'cloud-custodian'
        pubsub_snapshot_name = 'projects/cloud-custodian/snapshots/custodian'
        session_factory = self.replay_flight_data(
            'pubsub-snapshot-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-snapshot-dryrun',
             'resource': 'gcp.pubsub-snapshot'},
            session_factory=session_factory)

        pubsub_snapshot_resources = policy.run()
        self.assertEqual(pubsub_snapshot_resources[0]['name'], pubsub_snapshot_name)

    def test_pubsub_snapshot_delete(self):
        project_id = 'cloud-custodian'
        resource_name = 'projects/%s/snapshots/snapshot-to-delete' % project_id
        session_factory = self.replay_flight_data(
            'pubsub-snapshot-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-pubsub-snapshot-delete',
             'resource': 'gcp.pubsub-snapshot',
             'filters': [{'type': 'value',
                          'key': 'name',
                          'value': resource_name}],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], resource_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        resources = client.execute_query('list', {'project': 'projects/%s' % project_id})
        self.assertNotIn('snapshots', resources)
