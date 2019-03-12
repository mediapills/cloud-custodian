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
        factory = self.replay_flight_data('logsink', project_id)
        p = self.load_policy({
            'name': 'logsink',
            'resource': 'gcp.logsink'},
            session_factory=factory)
        resource = p.run()
        self.assertEqual(len(resource), 1)

    def test_get_log_sink(self):
        project_id = 'cloud-custodian'
        sink_name = "storage"
        factory = self.replay_flight_data(
            'logsink-resource', project_id)
        p = self.load_policy({'name': 'logsink', 'resource': 'gcp.logsink'},
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
