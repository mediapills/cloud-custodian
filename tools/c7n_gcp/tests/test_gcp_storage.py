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


class BucketTest(BaseTest):

    def test_bucket_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-query', project_id)
        p = self.load_policy({
            'name': 'all-buckets',
            'resource': 'gcp.bucket'
        }, session_factory=factory)

        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['id'], 'staging.cloud-custodian.appspot.com')
        self.assertEqual(resources[0]['storageClass'], 'STANDARD')

    def test_bucket_get(self):
        project_id = 'cloud-custodian'
        bucket_name = 'bucketstorage-1'
        factory = self.replay_flight_data(
            'bucket-get', project_id)
        p = self.load_policy({
            'name': 'bucket',
            'resource': 'gcp.bucket',
            'mode': {
                'type': 'gcp-audit',
                'methods': ['storage.buckets.create']
            }
        }, session_factory=factory)

        exec_mode = p.get_execution_mode()
        event = event_data('bucket-create.json')
        bucket = exec_mode.run(event, None)
        self.assertEqual(bucket[0]['name'], bucket_name)
        self.assertEqual(bucket[0]['id'], 'bucketstorage-1')
        self.assertEqual(bucket[0]['storageClass'], 'STANDARD')
        self.assertEqual(bucket[0]['location'], 'US')

    def test_bucket_set(self):
        project_id = 'cloud-custodian-190204'
        session_factory = self.replay_flight_data(
            'bucket-set', project_id=project_id)

        policy = self.load_policy({
            'name': 'gcp-bucket-update-storage-class',
            'resource': 'gcp.bucket',
            'filters': [{
                'type': 'value',
                'key': 'location',
                'op': 'regex',
                'value': 'US.*'
            }],
            'actions': [{
                'type': 'set',
                'class': 'NEARLINE',
                'retention-policy-seconds': 0,
                'versioning': True
            }]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['storageClass'], 'REGIONAL')
        self.assertEqual(resources[0]['retentionPolicy']['retentionPeriod'], '3155760000')
        self.assertFalse('versioning' not in resources[0])

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'project': project_id})

        self.assertEqual(result['items'][0]['storageClass'], 'NEARLINE')
        self.assertFalse('retentionPolicy' in result['items'])
        self.assertEqual(result['items'][0]['versioning']['enabled'], True)

    def test_validate_retention_and_versioning_coexistence(self):
        policy = self.load_policy({
            'name': 'gcp-bucket-update-storage-class',
            'resource': 'gcp.bucket',
            'actions': [{'type': 'set'}]})
        test_method = (policy.resource_manager.actions[0].
                       _validate_retention_and_versioning_coexistence)
        expected_error_message = ('Retention policies and Object Versioning are '
                                  'mutually exclusive features in Cloud Storage.')

        # preventing a wrong configuration from being set regardless of the processed resource
        resource = {}
        params = {'body': {
            'retentionPolicy': {'retentionPeriod': 86400},
            'versioning': {'enabled': True}
        }}
        self._call_method_expect_exception(test_method, resource, params, expected_error_message)

        # versioning is set enabled in the action while active retentionPolicy remains unchanged
        resource = {'versioning': {'enabled': False},
                    'retentionPolicy': {
                        'effectiveTime': '2019-08-06T07:38:15.729Z',
                        'retentionPeriod': '3155760000'}}
        params = {'body': {
            'versioning': {'enabled': True}
        }}
        self._call_method_expect_exception(test_method, resource, params, expected_error_message)

        # retentionPolicy is set enabled in the action while active versioning remains unchanged
        resource = {'versioning': {'enabled': True}}
        params = {'body': {
            'retentionPolicy': {'retentionPeriod': 86400}
        }}
        self._call_method_expect_exception(test_method, resource, params, expected_error_message)

    def _call_method_expect_exception(self, test_method, resource, params, expected_error_message):
        try:
            test_method(resource, params['body'])
            self.fail('No expected_error_message has been raised.')
        except ValueError as e:
            self.assertEqual(str(e), expected_error_message)

    def test_bucket_delete(self):
        project_id = 'new-project-26240'
        bucket_name = 'qwerty123567'
        session_factory = self.replay_flight_data(
            'bucket-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-delete',
             'resource': 'gcp.bucket',
             'filters': [{
                 'type': 'value',
                 'key': 'updated',
                 'op': 'greater-than',
                 'value_type': 'age',
                 'value': 365
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['id'], bucket_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'project': project_id})
        self.assertEqual(len(result['items']), 0)


class BucketAccessControlTest(BaseTest):

    def test_bucket_access_control_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-access-control-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-access-control',
             'resource': 'gcp.bucket-access-control'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['bucket'], 'staging.cloud-custodian.appspot.com')

    def test_bucket_access_control_get(self):
        project_id = 'cloud-custodian'
        bucket_name = 'bucketstorage-1'

        factory = self.replay_flight_data(
            'bucket-access-control-get', project_id)

        p = self.load_policy({
            'name': 'bucket-access-control-get',
            'resource': 'gcp.bucket-access-control',
            'mode': {
                'type': 'gcp-audit',
                'methods': ['storage.buckets.update']}},
            session_factory=factory)

        exec_mode = p.get_execution_mode()
        event = event_data('bucket-access-control-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['bucket'], bucket_name)

    def test_bucket_access_control_set(self):
        project_id = 'cloud-custodian'
        entity = 'user-yauhen_shaliou@comelfo.com'
        bucket_name = 'cloud-custodian.appspot.com'

        session_factory = self.replay_flight_data(
            'bucket-access-control-set', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-bucket-access-control-update-role',
             'resource': 'gcp.bucket-access-control',
             'filters': [{
                 'type': 'value',
                 'key': 'entity',
                 'value': entity
             }],
             'actions': [{
                 'type': 'set',
                 'role': 'OWNER'
             }]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['role'], 'READER')

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': bucket_name})
        self.assertEqual(result['items'][0]['role'], 'OWNER')

    def test_bucket_access_control_delete(self):
        project_id = 'new-project-26240'
        entity = 'user-yauhen_shaliou@comelfo.com'
        bucket_name = 'new-project-26240.appspot.com'

        session_factory = self.replay_flight_data(
            'bucket-access-control-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-access-control-delete',
             'resource': 'gcp.bucket-access-control',
             'filters': [{
                 'type': 'value',
                 'key': 'entity',
                 'value': entity
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['entity'], entity)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': bucket_name})

        self.assertEqual(len(result['items']), 2)


class BucketDefaultObjectAccessControlTest(BaseTest):

    def test_default_object_access_control_query(self):
        project_id = 'cloud-custodian'
        entity = 'project-owners-518122731295'
        factory = self.replay_flight_data('bucket-default-object-access-control-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-default-object-access-control',
             'resource': 'gcp.bucket-default-object-access-control'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['entity'], entity)

    def test_default_object_access_control_get(self):
        project_id = 'mitrop-custodian'
        entity = 'user-pavel_mitrafanau@epam.com'

        factory = self.replay_flight_data(
            'bucket-default-object-access-control-get', project_id)

        p = self.load_policy({'name': 'bucket-default-object-access-control-get',
                              'resource': 'gcp.bucket-default-object-access-control',
                              'mode': {
                                  'type': 'gcp-audit',
                                  'methods': ['storage.buckets.update']}
                              },
                             session_factory=factory)
        exec_mode = p.get_execution_mode()
        event = event_data('bucket-default-object-access-control-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['entity'], entity)

    def test_default_object_access_control_set(self):
        project_id = 'new-project-26240'
        entity = 'user-yauhen_shaliou@comelfo.com'
        bucket_name = 'new-project-26240.appspot.com'
        session_factory = self.replay_flight_data(
            'bucket-default-object-access-control-set', project_id=project_id)

        policy = self.load_policy({
            'name': 'gcp-bucket-default-access-control-update-role',
            'resource': 'gcp.bucket-default-object-access-control',
            'filters': [{
                'type': 'value',
                'key': 'entity',
                'value': entity
            }],
            'actions': [{
                'type': 'set',
                'role': 'OWNER'
            }]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['role'], 'READER')

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': bucket_name})
        self.assertEqual(result['items'][0]['role'], 'OWNER')

    def test_default_object_access_control_delete(self):
        project_id = 'new-project-26240'
        entity = 'user-yauhen_shaliou@comelfo.com'
        bucket_name = 'new-project-26240.appspot.com'
        session_factory = self.replay_flight_data(
            'bucket-default-object-access-control-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-default-access-control-delete',
             'resource': 'gcp.bucket-default-object-access-control',
             'filters': [{
                 'type': 'value',
                 'key': 'entity',
                 'value': entity
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['entity'], entity)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': bucket_name})

        self.assertEqual(len(result['items']), 4)


class BucketObjectTest(BaseTest):

    def test_bucket_object_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-object-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-object',
             'resource': 'gcp.bucket-object'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], 'commit-example.txt')

    def test_bucket_object_get(self):
        project_id = 'new-project-26240'
        bucket_name = 'new-project-26240.appspot.com'
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
        event = event_data('bucket-object-access-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['bucket'], bucket_name)
        self.assertEqual(instance[0]['name'], name)

    def test_bucket_object_set(self):
        project_id = 'new-project-26240'
        session_factory = self.replay_flight_data(
            'bucket-object-update-cache-control', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-object-update-content-type',
             'resource': 'gcp.bucket-object',
             'filters': [{
                 'type': 'value',
                 'key': 'timeCreated',
                 'op': 'greater-than',
                 'value_type': 'age',
                 'value': 31
             }],
             'actions': [{
                 'type': 'set',
                 'cache_control': 'max-age=3600'
             }]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['cacheControl'], 'public')

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': 'new-project-26240.appspot.com'})

        self.assertEqual(result['items'][0]['cacheControl'], 'max-age=3600')

    def test_bucket_object_delete(self):
        project_id = 'new-project-26240'
        name = 'text.txt'
        session_factory = self.replay_flight_data(
            'bucket-object-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-object-delete',
             'resource': 'gcp.bucket-object',
             'filters': [{
                 'type': 'value',
                 'key': 'timeCreated',
                 'op': 'greater-than',
                 'value_type': 'age',
                 'value': 31
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['name'], name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': 'new-project-26240.appspot.com'})

        self.assertNotIn('items', result)


class BucketObjectAccessControlTest(BaseTest):

    def test_object_access_control_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('bucket-object-access-control-query', project_id)
        p = self.load_policy(
            {'name': 'all-bucket-object-access-control',
             'resource': 'gcp.bucket-object-access-control'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['object'], 'commit-example.txt')

    def test_object_access_control_get(self):
        project_id = 'new-project-26240'
        bucket_name = 'new-project-26240.appspot.com'
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
        event = event_data('bucket-object-access-update.json')
        instance = exec_mode.run(event, None)
        self.assertEqual(instance[0]['bucket'], bucket_name)
        self.assertEqual(instance[0]['object'], name)

    def test_object_access_control_set(self):
        project_id = 'cloud-custodian'
        entity = 'user-yauhen_shaliou@comelfo.com'
        object_name = 'text.txt'
        bucket_name = 'cloud-custodian.appspot.com'
        session_factory = self.replay_flight_data(
            'bucket-object-access-control-update-role', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-object-access-control-update-role',
             'resource': 'gcp.bucket-object-access-control',
             'filters': [{
                 'type': 'value',
                 'key': 'entity',
                 'value': entity
             }],
             'actions': [{
                 'type': 'set',
                 'role': 'OWNER'
             }]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['role'], 'READER')

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': bucket_name,
                     'object': object_name})
        self.assertEqual(result['items'][0]['role'], 'OWNER')

    def test_object_access_control_delete(self):
        project_id = 'new-project-26240'
        entity = 'user-yauhen_shaliou@comelfo.com'
        object_name = 'text.txt'
        bucket_name = 'new-project-26240.appspot.com'

        session_factory = self.replay_flight_data(
            'bucket-object-access-control-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-bucket-object-access-control-delete',
             'resource': 'gcp.bucket-object-access-control',
             'filters': [{
                 'type': 'value',
                 'key': 'entity',
                 'value': entity
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        resources = policy.run()
        self.assertEqual(resources[0]['entity'], entity)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        result = client.execute_query(
            'list', {'bucket': bucket_name,
                     'object': object_name})

        self.assertEqual(len(result['items']), 4)
