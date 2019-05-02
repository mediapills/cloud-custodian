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


class BucketTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-query', project_id)
        p = self.load_policy(
            {'name': 'all-buckets',
             'resource': 'gcp.bucket'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['id'], "staging.cloud-custodian.appspot.com")
        self.assertEqual(resources[0]['storageClass'], "STANDARD")

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        bucket_name = "staging.cloud-custodian.appspot.com"
        factory = self.replay_flight_data(
            'bucket-get-resource', project_id)
        p = self.load_policy({'name': 'bucket', 'resource': 'gcp.bucket'},
                             session_factory=factory)
        bucket = p.resource_manager.get_resource({
            "bucket_name": bucket_name,
        })
        self.assertEqual(bucket['name'], bucket_name)
        self.assertEqual(bucket['id'], "staging.cloud-custodian.appspot.com")
        self.assertEqual(bucket['storageClass'], "STANDARD")
        self.assertEqual(bucket['location'], "EU")


class BucketAccessControlTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'  # 'test-project-232910'
        factory = self.replay_flight_data('bucket-access-control-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-access-control',
             'resource': 'gcp.bucket-access-control'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['bucket'], 'staging.cloud-custodian.appspot.com')

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        bucket_name = "staging.cloud-custodian.appspot.com"
        entity = "project-editors-518122731295"

        factory = self.replay_flight_data(
            'bucket-access-control-get', project_id)
        p = self.load_policy({
            'name': 'bucket-access-control-get',
            'resource': 'gcp.bucket-access-control'
        },
            session_factory=factory)

        instance = p.resource_manager.get_resource({
            "bucket_name": bucket_name,
            "entity": entity,
        })
        self.assertEqual(instance['bucket'], bucket_name)


class DefaultObjectAccessControlTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'  # 'test-project-232910'
        entity = "project-owners-518122731295"
        factory = self.replay_flight_data('bucket-default-object-access-control-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-default-object-access-control',
             'resource': 'gcp.bucket-default-object-access-control'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['entity'], entity)

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        bucket_name = "staging.cloud-custodian.appspot.com"
        entity = "project-editors-518122731295"

        factory = self.replay_flight_data(
            'bucket-default-object-access-control-get', project_id)
        p = self.load_policy({
            'name': 'bucket-default-object-access-control-get',
            'resource': 'gcp.bucket-default-object-access-control'
        },
            session_factory=factory)

        instance = p.resource_manager.get_resource({
            "bucket_name": bucket_name,
            "entity": entity,
        })
        self.assertEqual(instance['bucket_name'], bucket_name)
        self.assertEqual(instance['entity'], entity)


class BucketObjectTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-object-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-object',
             'resource': 'gcp.bucket-object'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], "commit-example.txt")

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        bucket_name = "staging.cloud-custodian.appspot.com"
        name = "commit-example.txt"

        factory = self.replay_flight_data(
            'bucket-object-get', project_id)
        p = self.load_policy({
            'name': 'bucket-object-get',
            'resource': 'gcp.bucket-object'
        },
            session_factory=factory)

        instance = p.resource_manager.get_resource({
            "bucket_name": bucket_name,
            "name": name
        })
        self.assertEqual(instance['bucket'], bucket_name)
        self.assertEqual(instance['name'], name)


class BucketObjectAccessControlTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-object-access-control-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-object-access-control',
             'resource': 'gcp.bucket-object-access-control'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['object'], "commit-example.txt")

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        bucket_name = "staging.cloud-custodian.appspot.com"
        name = "commit-example.txt"
        entity = "project-owners-518122731295"

        factory = self.replay_flight_data(
            'bucket-object-access-control-get', project_id)
        p = self.load_policy({
            'name': 'bucket-object-access-control-get',
            'resource': 'gcp.bucket-object-access-control'
        },
            session_factory=factory)

        instance = p.resource_manager.get_resource({
            "bucket_name": bucket_name,
            "name": name,
            "entity": entity
        })
        self.assertEqual(instance['bucket'], bucket_name)
        self.assertEqual(instance['object'], name)


class BucketNotificationTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-notification-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-notification',
             'resource': 'gcp.bucket-notification'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['id'], "1")

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        bucket_name = "staging.cloud-custodian.appspot.com"
        notification_id = "1"

        factory = self.replay_flight_data(
            'bucket-notification-get', project_id)
        p = self.load_policy({
            'name': 'bucket-notification-get',
            'resource': 'gcp.bucket-notification'
        },
            session_factory=factory)

        instance = p.resource_manager.get_resource({
            "bucket_name": bucket_name,
            "notification_id": notification_id,
        })
        self.assertIn(bucket_name, instance['selfLink'])
        self.assertEqual(instance['id'], notification_id)


class BucketServiceAccountTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-service-account-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-service-account',
             'resource': 'gcp.bucket-service-account'},
            session_factory=factory)
        resources = p.run()
        self.assertIn('email_address', resources[0].keys())

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data(
            'bucket-service-account-get-resource', project_id)
        p = self.load_policy({'name': 'bucket-service-account', 'resource': 'gcp.bucket-service-account'},
                             session_factory=factory)
        bucket = p.resource_manager.get_resource({
            "project_id": project_id,
        })
        self.assertIn('email_address', bucket.keys())

