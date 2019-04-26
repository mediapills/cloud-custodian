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
        bucket_name = "bucketstorage-1"
        factory = self.replay_flight_data(
            'bucket-get-resource', project_id)
        p = self.load_policy({'name': 'bucket',
                              'resource': 'gcp.bucket',
                              'mode': {
                                  'type': 'gcp-audit',
                                  'methods': ['storage.buckets.create']}
                              },
                             session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('cs-bucket-create.json')
        bucket = exec_mode.run(event, None)
        self.assertEqual(bucket[0]['name'], bucket_name)
        self.assertEqual(bucket[0]['id'], "bucketstorage-1")
        self.assertEqual(bucket[0]['storageClass'], "STANDARD")
        self.assertEqual(bucket[0]['location'], "US")


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
        bucket_name = 'bucketstorage-1'

        factory = self.replay_flight_data(
            'bucket-access-control-get', project_id)

        p = self.load_policy({'name': 'bucket-access-control-get',
                              'resource': 'gcp.bucket-access-control',
                              'mode': {
                                  'type': 'gcp-audit',
                                  'methods': ['storage.buckets.update']}
                              },
                             session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('cs-bucket-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['bucket'], bucket_name)


class BucketDefaultObjectAccessControlTest(BaseTest):

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
        bucket_name = "cloud-custodian.appspot.com"

        factory = self.replay_flight_data(
            'bucket-access-control-get', project_id)

        p = self.load_policy({'name': 'bucket-default-object-access-control-get',
                              'resource': 'gcp.bucket-default-object-access-control',
                              'mode': {
                                  'type': 'gcp-audit',
                                  'methods': ['storage.buckets.update']}
                              },
                             session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('cs-bucket-access-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['bucket_name'], bucket_name)


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
        bucket_name = "cloud-custodian.appspot.com"
        name = '1.py'
        factory = self.replay_flight_data(
            'bucket-object-get', project_id)

        p = self.load_policy({'name': 'bucket-object-get',
                              'resource': 'gcp.bucket-object',
                              'mode': {
                                  'type': 'gcp-audit',
                                  'methods': ['storage.buckets.update']}
                              },
                             session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('cs-bucket-object-access-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['bucket'], bucket_name)
        self.assertEqual(instance[0]['name'], name)


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
        bucket_name = "cloud-custodian.appspot.com"
        name = '1.py'
        factory = self.replay_flight_data(
            'bucket-object-access-control-get', project_id)

        p = self.load_policy({'name': 'bucket-object-access-control-get',
                              'resource': 'gcp.bucket-object-access-control',
                              'mode': {
                                  'type': 'gcp-audit',
                                  'methods': ['storage.buckets.update']}
                              },
                             session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('cs-bucket-object-access-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['bucket'], bucket_name)
        self.assertEqual(instance[0]['object'], name)
