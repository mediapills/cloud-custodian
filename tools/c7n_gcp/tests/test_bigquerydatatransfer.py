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
import os
import json
from gcp_common import BaseTest


class BigQueryDataTransferConfigTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data(
            'bq-datatransfer-transfer-config-get', project_id=project_id)

        p = self.load_policy({
            'name': 'bq-datatransfer-transfer-config-get',
            'resource': 'gcp.bq-datatransfer-transfer-config'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['state'], 'SUCCEEDED')
        self.assertEqual(resources[0]['dataSourceId'], 'google_cloud_storage')

    def test_delete(self):
        project_id = 'cloud-custodian'

        factory = self.replay_flight_data(
            'bq-datatransfer-transfer-config-delete', project_id=project_id)

        p = self.load_policy(
            {'name': 'bq-datatransfer-transfer-config-delete',
             'resource': 'gcp.bq-datatransfer-transfer-config',
             'filters': [{
                 'type': 'value',
                 'key': 'state',
                 'value': 'FAILED',
             }],
             'actions': [{
                 'type': 'delete'
             }]},
            session_factory=factory)

        resources = p.run()
        self.assertEqual(len(resources), 1)

        files_dir = os.path.join(os.path.dirname(__file__),
                                 'data', 'flights', 'bq-datatransfer-transfer-config-delete')

        files_paths = [file_path for file_path in os.listdir(files_dir)
                       if file_path.__contains__('delete')]

        self.assertEqual(1, len(files_paths))

        for file_path in files_paths:
            with open(os.path.join(files_dir, file_path), 'rt') as file:
                response = json.load(file)
                self.assertEqual('200', response['headers']['status'])
