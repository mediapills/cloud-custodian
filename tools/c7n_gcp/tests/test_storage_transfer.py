# Copyright 2018 Capital One Services, LLC
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


class StorageTransferJobTest(BaseTest):

    def test_query(self):
        factory = self.replay_flight_data('st-transfer-job-query')
        p = self.load_policy({
            'name': 'st-transfer-job',
            'resource': 'gcp.st-transfer-job'},
            session_factory=factory)
        resources = p.run()

        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], 'transferJobs/12533737323236783615')
        self.assertEqual(resources[0]['status'], 'ENABLED')


class StorageTransferJobPatchTest(BaseTest):

    def test_set_status(self):
        project_id = 'cloud-custodian'

        session_factory = self.replay_flight_data(
            'storage-transfer-update', project_id=project_id)

        policy = self.load_policy({
            'name': 'storage-transfer-update',
            'resource': 'gcp.st-transfer-job',
            'actions': [{
                'type': 'set',
                'status': 'DISABLED'
            }]},
            session_factory=session_factory)

        resources = policy.run()

        self.assertEqual(1, len(resources))

        files_dir = os.path.join(
            os.path.dirname(__file__),
            'data', 'flights', 'storage-transfer-update')

        files_paths = [file_path for file_path in os.listdir(files_dir)
                       if file_path.__contains__('2395599000273777125_1')]

        self.assertEqual(1, len(files_paths))

        for file_path in files_paths:
            with open(os.path.join(files_dir, file_path), 'rt') as file:
                response = json.load(file)
                self.assertEqual("DISABLED", response['body']['status'])
