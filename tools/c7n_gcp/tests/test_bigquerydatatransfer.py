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


class BigQueryDataTransferTest(BaseTest):

    def test_query(self):
        project_id = 'new-project-26240'
        factory = self.replay_flight_data('bq-datatransfer-get', project_id=project_id)
        p = self.load_policy({
            'name': 'bq-datatransfer-get',
            'resource': 'gcp.bq-datatransfer'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['state'], 'SUCCEEDED')
        self.assertEqual(resources[0]['dataSourceId'], 'google_cloud_storage')

