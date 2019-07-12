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

import re

from gcp_common import BaseTest
from time import sleep

from googleapiclient.errors import HttpError


class AppEngineAppTest(BaseTest):

    def test_app_query(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/{}'.format(project_id)
        session_factory = self.replay_flight_data(
            'app-engine-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-dryrun',
             'resource': 'gcp.app-engine'},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], app_name)

    def test_app_get(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/' + project_id
        session_factory = self.replay_flight_data(
            'app-engine-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-dryrun',
             'resource': 'gcp.app-engine'},
            session_factory=session_factory)

        resource = policy.resource_manager.get_resource(
            {'resourceName': app_name})
        self.assertEqual(resource['name'], app_name)

    def test_app_start(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/' + project_id
        session_factory = self.replay_flight_data(
            'app-engine-start', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-start',
             'resource': 'gcp.app-engine',
             'actions': [{'type': 'start'}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], app_name)

        if self.recording:
            sleep(1)

        app_short_name = resources[0]['id']
        client = policy.resource_manager.get_client()
        result = client.execute_query('get', {'appsId': app_short_name})
        self.assertEqual(result['servingStatus'], 'SERVING')

    def test_app_stop(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/' + project_id
        session_factory = self.replay_flight_data(
            'app-engine-stop', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-stop',
             'resource': 'gcp.app-engine',
             'actions': [{'type': 'stop'}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], app_name)

        if self.recording:
            sleep(1)

        app_short_name = resources[0]['id']
        client = policy.resource_manager.get_client()
        result = client.execute_query('get', {'appsId': app_short_name})
        self.assertEqual(result['servingStatus'], 'USER_DISABLED')

    def test_app_set(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/' + project_id
        session_factory = self.replay_flight_data(
            'app-engine-set', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-set',
             'resource': 'gcp.app-engine',
             'actions': [{'type': 'set',
                          'split-health-checks': True,
                          'use-container-optimized-os': False}]},
            session_factory=session_factory)

        resources = policy.run()
        self.assertEqual(resources[0]['name'], app_name)

        if self.recording:
            sleep(1)

        app_short_name = resources[0]['id']
        client = policy.resource_manager.get_client()
        result = client.execute_query('get', {'appsId': app_short_name})
        self.assertEqual(result['featureSettings']['splitHealthChecks'], True)
        self.assertTrue('useContainerOptimizedOs' not in result['featureSettings'])


class AppEngineCertificateTest(BaseTest):

    def test_certificate_query(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/{}'.format(project_id)
        certificate_id = '12277184'
        certificate_name = '{}/authorizedCertificates/{}'.format(app_name, certificate_id)
        session_factory = self.replay_flight_data(
            'app-engine-certificate-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-certificate-dryrun',
             'resource': 'gcp.app-engine-certificate'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(resources[0]['name'], certificate_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], app_name)

    def test_certificate_get(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/' + project_id
        certificate_id = '12277184'
        certificate_name = '{}/authorizedCertificates/{}'.format(app_name, certificate_id)
        session_factory = self.replay_flight_data(
            'app-engine-certificate-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-certificate-dryrun',
             'resource': 'gcp.app-engine-certificate'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resource = policy.resource_manager.get_resource(
            {'resourceName': certificate_name})
        self.assertEqual(resource['name'], certificate_name)
        self.assertEqual(resource[parent_annotation_key]['name'], app_name)


class AppEngineDomainTest(BaseTest):

    def test_domain_query(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/{}'.format(project_id)
        domain_id = 'gcp-li.ga'
        domain_name = '{}/authorizedDomains/{}'.format(app_name, domain_id)
        session_factory = self.replay_flight_data(
            'app-engine-domain-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-domain-dryrun',
             'resource': 'gcp.app-engine-domain'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(resources[0]['name'], domain_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], app_name)


class AppEngineDomainMappingTest(BaseTest):

    def test_domain_mapping_query(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/{}'.format(project_id)
        domain_mapping_id = 'alex.gcp-li.ga'
        domain_mapping_name = '{}/domainMappings/{}'.format(app_name, domain_mapping_id)
        session_factory = self.replay_flight_data(
            'app-engine-domain-mapping-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-domain-mapping-dryrun',
             'resource': 'gcp.app-engine-domain-mapping'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(resources[0]['name'], domain_mapping_name)
        self.assertEqual(resources[0][parent_annotation_key]['name'], app_name)

    def test_domain_mapping_get(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/' + project_id
        domain_mapping_id = 'alex.gcp-li.ga'
        domain_mapping_name = '{}/domainMappings/{}'.format(app_name, domain_mapping_id)
        session_factory = self.replay_flight_data(
            'app-engine-domain-mapping-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-domain-mapping-dryrun',
             'resource': 'gcp.app-engine-domain-mapping'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resource = policy.resource_manager.get_resource(
            {'resourceName': domain_mapping_name})
        self.assertEqual(resource['name'], domain_mapping_name)
        self.assertEqual(resource[parent_annotation_key]['name'], app_name)

    def test_domain_mapping_delete(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/' + project_id
        domain_mapping_id = 'outdated.gcp-li.ga'
        domain_mapping_name = '{}/domainMappings/{}'.format(app_name, domain_mapping_id)
        session_factory = self.replay_flight_data(
            'app-engine-domain-mapping-delete', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-domain-mapping-delete',
             'resource': 'gcp.app-engine-domain-mapping',
             'filters': [{
                 'type': 'value',
                 'key': 'id',
                 'value': domain_mapping_id
             }],
             'actions': [{'type': 'delete'}]},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resource = policy.run()[0]
        self.assertEqual(resource['name'], domain_mapping_name)
        self.assertEqual(resource[parent_annotation_key]['name'], app_name)

        if self.recording:
            sleep(1)

        client = policy.resource_manager.get_client()
        app_short_name = project_id
        try:
            result = client.execute_query('get', {'appsId': app_short_name,
                                                  'domainMappingsId': domain_mapping_id})
            self.fail('found deleted resource: %s' % result)
        except HttpError as e:
            self.assertTrue(re.match(".*Domain mapping '.+?' not found.*", str(e)))


class AppEngineFirewallIngressRuleTest(BaseTest):

    def test_firewall_ingress_rule_query(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/{}'.format(project_id)
        rule_priority = 2147483647
        session_factory = self.replay_flight_data(
            'app-engine-firewall-ingress-rule-query', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-firewall-ingress-rule-dryrun',
             'resource': 'gcp.app-engine-firewall-ingress-rule'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resources = policy.run()
        self.assertEqual(resources[0]['priority'], rule_priority)
        self.assertEqual(resources[0][parent_annotation_key]['name'], app_name)

    def test_firewall_ingress_rule_get(self):
        project_id = 'cloud-custodian'
        app_name = 'apps/{}'.format(project_id)
        rule_priority = 2147483647
        rule_priority_full = '{}/firewall/ingressRules/{}'.format(app_name, rule_priority)
        session_factory = self.replay_flight_data(
            'app-engine-firewall-ingress-rule-get', project_id=project_id)

        policy = self.load_policy(
            {'name': 'gcp-app-engine-firewall-ingress-rule-dryrun',
             'resource': 'gcp.app-engine-firewall-ingress-rule'},
            session_factory=session_factory)
        parent_annotation_key = policy.resource_manager.resource_type.get_parent_annotation_key()

        resource = policy.resource_manager.get_resource(
            {'resourceName': rule_priority_full})
        self.assertEqual(resource['priority'], rule_priority)
        self.assertEqual(resource[parent_annotation_key]['name'], app_name)
