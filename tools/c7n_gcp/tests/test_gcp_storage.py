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
