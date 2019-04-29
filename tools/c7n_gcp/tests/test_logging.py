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


class LogProjectSinkTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('log-project-sink-query', project_id)
        p = self.load_policy({
            'name': 'log-project-sink',
            'resource': 'gcp.log-project-sink'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 1)

    def test_get_project_sink(self):
        project_id = 'cloud-custodian'
        sink_name = "storage"
        factory = self.replay_flight_data(
            'log-project-sink-resource', project_id)
        p = self.load_policy({
            'name': 'log-project-sink',
            'resource': 'gcp.log-project-sink'
        }, session_factory=factory)
        sink = p.resource_manager.get_resource({
            "name": sink_name,
            "project_id": project_id,
        })
        self.assertEqual(sink['name'], sink_name)


class LogSinkTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('log-sink', project_id)
        p = self.load_policy({
            'name': 'log-sink',
            'resource': 'gcp.log-sink'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 1)

    def test_get_log_sink(self):
        project_id = 'cloud-custodian'
        sink_name = "storage"
        factory = self.replay_flight_data(
            'log-sink-resource', project_id)
        p = self.load_policy({'name': 'log-sink', 'resource': 'gcp.log-sink'},
                             session_factory=factory)
        sink = p.resource_manager.get_resource({
            "name": sink_name,
            "project_id": project_id,
        })
        self.assertEqual(sink['name'], sink_name)


class LogProjectMetricTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('log-project-metric-get', project_id)
        p = self.load_policy({
            'name': 'log-project-metric',
            'resource': 'gcp.log-project-metric'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 1)

    def test_get_project_metric(self):
        project_id = 'cloud-custodian'
        metric_name = "test"
        factory = self.replay_flight_data(
            'log-project-metric-query', project_id)
        p = self.load_policy({
            'name': 'log-project-metric',
            'resource': 'gcp.log-project-metric'
        }, session_factory=factory)
        metric = p.resource_manager.get_resource({
            "name": metric_name,
            "project_id": project_id,
        })
        self.assertEqual(metric['name'], metric_name)


class LogProjectTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('log-project', project_id)
        p = self.load_policy({
            'name': 'log-project',
            'resource': 'gcp.log-project'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 3)


class LogProjectExclusionTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('log-project-exclusion', project_id)
        p = self.load_policy({
            'name': 'log-project-exclusion',
            'resource': 'gcp.log-project-exclusion'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 1)

    def test_get_project_exclusion(self):
        project_id = 'cloud-custodian'
        exclusion_name = "exclusions"
        factory = self.replay_flight_data(
            'log-project-exclusion-get', project_id)

        p = self.load_policy(
            {
                'name': 'log-project-exclusion-get',
                'resource': 'gcp.log-project-exclusion'
            },
            session_factory=factory)

        resource = p.resource_manager.get_resource({
            "exclusion_id": exclusion_name,
            "project_id": project_id,
        })
        self.assertEqual(resource['name'], exclusion_name)


class LogExclusionTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('log-exclusion', project_id)
        p = self.load_policy({
            'name': 'log-exclusion',
            'resource': 'gcp.log-exclusion'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 1)

    def test_get_project_exclusion(self):
        project_id = 'cloud-custodian'
        exclusion_name = "exclusions"
        type = "projects"
        factory = self.replay_flight_data(
            'log-exclusion-get', project_id)

        p = self.load_policy(
            {
                'name': 'log-exclusion-get',
                'resource': 'gcp.log-exclusion'
            },
            session_factory=factory)

        resource = p.resource_manager.get_resource({
            "exclusion_id": exclusion_name,
            "project_id": project_id,
            "type": type,
        })
        self.assertEqual(resource['name'], exclusion_name)


class LogMonitoredResourceDescriptorTest(BaseTest):

    def test_query(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('log-monitored-resource-descriptor', project_id)
        p = self.load_policy({
            'name': 'log-monitored-resource-descriptor',
            'resource': 'gcp.log-monitored-resource-descriptor'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 2)
        self.assertEqual(resource[0]['displayName'], "GCE VM Instance")


class LogEntriesTest(BaseTest):

    def test_query_projects(self):
        factory = self.replay_flight_data('log-entries-projects')
        p = self.load_policy({
            'name': 'log-entries-projects',
            'query': 'projects/custodian-test-project-0',
            'resource': 'gcp.log-entries'},
            session_factory=factory)
        resource = p.run()
        self.assertGreater(len(resource), 1)

    def test_query_organizations(self):
        factory = self.replay_flight_data('log-entries-organizations')
        p = self.load_policy({
            'name': 'log-entries-organizations',
            'query': 'organizations/926683928810',
            'resource': 'gcp.log-entries'},
            session_factory=factory)
        resource = p.run()
        self.assertGreater(len(resource), 1)

    def test_query_billing_accounts(self):
        factory = self.replay_flight_data('log-entries-billing-accounts')
        p = self.load_policy({
            'name': 'log-entries-billing-accounts',
            'query': 'billingAccounts/016591-0C32EA-F3D1B3',
            'resource': 'gcp.log-entries'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 0)

    def test_query_folders(self):
        factory = self.replay_flight_data('log-entries-folders')
        p = self.load_policy({
            'name': 'log-entries-folders',
            'query': 'folders/112838955399',
            'resource': 'gcp.log-entries'},
            session_factory=factory)
        resource = p.run()
        self.assertGreater(len(resource), 1)
