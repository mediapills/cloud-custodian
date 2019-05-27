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


class DialogFlowAgentTest(BaseTest):

    def test_dialog_flow_agent_query(self):
        project_id = 'custodian-test-project-0'
        factory = self.replay_flight_data('df-agent-query',
                                          project_id=project_id)
        policy = self.load_policy(
            {'name': 'all-df-agents',
             'resource': 'gcp.dialogflow-agent'},
            session_factory=factory)
        resources = policy.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['defaultLanguageCode'], 'en')
        self.assertEqual(resources[0]['matchMode'], 'MATCH_MODE_HYBRID')


class DialogFlowEntityTypeTest(BaseTest):

    def test_dialog_flow_agent_entuty_type_query(self):
        project_id = 'custodian-test-project-0'
        factory = self.replay_flight_data('df-agent-entity-types-query',
                                          project_id=project_id)
        policy = self.load_policy(
            {'name': 'all-df-agent-entity-types',
             'resource': 'gcp.dialogflow-entity-type'},
            session_factory=factory)
        resources = policy.run()
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0]['displayName'], 'GoogleEntity')
        self.assertEqual(resources[1]['displayName'], 'CustodianEntity')
        self.assertEqual(len(resources[1]['entities']), 2)
        self.assertEqual(resources[1]['entities'][0]['value'], 'Custodian Entity')

    def test_dialog_flow_agent_entuty_type_get(self):
        factory = self.record_flight_data('df-agent-entity-types-get')
        policy = self.load_policy(
            {'name': 'df-agent-entity-types-query',
             'resource': 'gcp.dialogflow-entity-type',
             'mode': {
                 'type': 'gcp-audit',
                 'methods': []
             }},
            session_factory=factory)
        exec_mode = policy.get_execution_mode()
        event = event_data('df-agent-entity-types-get.json')
        instances = exec_mode.run(event, None)
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0]['kind'], 'compute#address')
        self.assertEqual(instances[0]['address'], '35.202.198.74')


class DialogFlowIntentTest(BaseTest):

    def test_dialog_flow_intent_query(self):
        project_id = 'custodian-test-project-0'
        factory = self.replay_flight_data('df-agent-intents-query',
                                          project_id=project_id)
        policy = self.load_policy(
            {'name': 'all-df-agent-intents',
             'resource': 'gcp.dialogflow-intent'},
            session_factory=factory)
        resources = policy.run()
        self.assertEqual(len(resources), 3)
        self.assertEqual(resources[1]['events'][0], 'WELCOME')
