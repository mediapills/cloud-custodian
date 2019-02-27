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

import time
from gcp_common import BaseTest


class SqlInstanceDatabaseTest(BaseTest):

    def test_delete_instance_database(self):
        project_id = 'cloud-custodian'
        instance_name = 'custodian-sql'
        database_name = 'custodian'
        factory = self.replay_flight_data('sqlinstancedatabase-delete', project_id=project_id)

        p = self.load_policy(
            {'name': 'sql-instance-database-delete',
             'resource': 'gcp.sql-instance-database',
             'query': [{'instance': instance_name}],
             'filters': [{'type': 'value', 'key': 'name', 'op': 'regex', 'value': '^%s$' % database_name}],
             'actions': [{'type':'delete'}]},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        if self.recording:
            time.sleep(1)
        client = p.resource_manager.get_client()
        result = client.execute_query(
            'list', {'project': project_id,
                     'instance': instance_name})
        remaining_database_names = list(map(lambda item: item['name'], result['items']))
        self.assertFalse(instance_name in remaining_database_names)
