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


class TestTagManagerAccounts(BaseTest):

    def test_accounts_query(self):
        session_factory = self.record_flight_data(
            'tagmanager-account')

        policy = self.load_policy(
            {
                'name': 'tagmanager-accounts-query',
                'resource': 'gcp.tagmanager-account'
            },
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(len(resources), 1)

    def test_accounts_get(self):
        accountId = "4701444124"

        session_factory = self.record_flight_data(
            'tagmanager-account-get')

        policy = self.load_policy(
            {
                'name': 'tagmanager-account-get',
                'resource': 'gcp.tagmanager-account'
            },
            session_factory=session_factory)

        resource = policy.resource_manager.get_resource({
            "accountId": accountId,
        })

        self.assertEqual(resource['accountId'], "accounts/{}".format(accountId))
