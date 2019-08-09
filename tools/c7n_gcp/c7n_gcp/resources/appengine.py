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

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo

from c7n.utils import local_session, type_schema


@resources.register('app-engine')
class AppEngineApp(QueryResourceManager):
    """GCP resource: https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps
    """
    class resource_type(TypeInfo):
        service = 'appengine'
        version = 'v1'
        component = 'apps'
        enum_spec = ('get', '[@]', None)
        scope = None
        id = 'id'

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', {'appsId': re.match('apps/(.*)',
                    resource_info['resourceName']).group(1)})

    def get_resource_query(self):
        return {'appsId': local_session(self.session_factory).get_default_project()}


@AppEngineApp.action_registry.register('set')
class AppEngineSet(MethodAction):
    """
    `Patches <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps/patch>`_
    App settings.

    If 'Split health checks' or 'Use Container-Optimized OS' is disabled, the key is removed from
    the resource rather than being marked as `false`.

    The 'split-health-check' flag controls if split health checks ('readinessCheck'
    and 'livenessCheck' at an app.yaml level) should be used instead of the legacy
    health checks ('healthCheck')

    The 'use-container-optimised-os' flag enables the use if Container-Optimized OS
    base image for VMs, rather than a base Debian image. Before patching the setting,
    make sure it is enabled for your project, otherwise the update `operation
    <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.operations/list>`_
    will fail although the policy will show no errors.

    The 'serving-status' flag sets 'servingStatus' either to 'SERVING' or 'USER_DISABLED'.

    In case any additional settings are needed to be included, please note how the 'updateMask'
    property is formed.

    .. code-block:: yaml

        policies:
          - name: gcp-app-engine-set
            resource: gcp.app-engine
            actions:
              - type: set
                split-health-checks: true
                use-container-optimized-os: true
                serving-status: true
    """
    schema = type_schema('set',
                         **{
                             'additionalProperties': False,
                             'minProperties': 1,
                             'split-health-checks': {'type': 'boolean'},
                             'use-container-optimized-os': {'type': 'boolean'},
                             'serving-status': {'type': 'boolean'}
                         })
    method_spec = {'op': 'patch'}

    def get_resource_params(self, m, r):
        params = {'appsId': r['id'], 'body': {}}
        body = params['body']
        if 'split-health-checks' in self.data or 'use-container-optimized-os' in self.data:
            body['featureSettings'] = {}
        if 'split-health-checks' in self.data:
            body['featureSettings']['splitHealthChecks'] = self.data['split-health-checks']
            self.extend_update_mask(params, 'feature_settings.split_health_checks')
        if 'use-container-optimized-os' in self.data:
            body['featureSettings']['useContainerOptimizedOs'] = self.data[
                'use-container-optimized-os']
            self.extend_update_mask(params, 'feature_settings.use_container_optimized_os')
        if 'serving-status' in self.data:
            body['servingStatus'] = ('SERVING' if self.data['serving-status']
                                     else 'USER_DISABLED')
            self.extend_update_mask(params, 'serving_status')
        return params

    def extend_update_mask(self, params, field_to_extend_with):
        """
        If the 'updateMask' key exists in `params`, concatenates the existing value at to the
        provided `field_to_extend_with` and updates the value at the key, otherwise simply writes
        `field_to_extend_with`.

        :param params: a dictionary to update 'updateMask' in
        :param field_to_extend_with: a value to concatenate or use as is
        """
        params['updateMask'] = (params['updateMask'] + ',' + field_to_extend_with
                                if 'updateMask' in params else field_to_extend_with)


@resources.register('app-engine-certificate')
class AppEngineCertificate(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.authorizedCertificates
    """
    def _get_parent_resource_info(self, child_instance):
        return {'resourceName': re.match(
            '(apps/.*?)/authorizedCertificates/.*', child_instance['name']).group(1)}

    class resource_type(ChildTypeInfo):
        service = 'appengine'
        version = 'v1'
        component = 'apps.authorizedCertificates'
        enum_spec = ('list', 'certificates[]', None)
        scope = None
        id = 'id'
        parent_spec = {
            'resource': 'app-engine',
            'child_enum_params': {
                ('id', 'appsId')
            }
        }

        @staticmethod
        def get(client, resource_info):
            apps_id, cert_id = re.match('apps/(.*?)/authorizedCertificates/(.*)',
                                        resource_info['resourceName']).groups()
            return client.execute_query('get', {'appsId': apps_id,
                                                'authorizedCertificatesId': cert_id})


@resources.register('app-engine-domain')
class AppEngineDomain(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.authorizedDomains
    """
    class resource_type(ChildTypeInfo):
        service = 'appengine'
        version = 'v1'
        component = 'apps.authorizedDomains'
        enum_spec = ('list', 'domains[]', None)
        scope = None
        id = 'id'
        parent_spec = {
            'resource': 'app-engine',
            'child_enum_params': {
                ('id', 'appsId')
            }
        }


@resources.register('app-engine-domain-mapping')
class AppEngineDomainMapping(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.domainMappings
    """
    def _get_parent_resource_info(self, child_instance):
        return {'resourceName': re.match(
            '(apps/.*?)/domainMappings/.*', child_instance['name']).group(1)}

    class resource_type(ChildTypeInfo):
        service = 'appengine'
        version = 'v1'
        component = 'apps.domainMappings'
        enum_spec = ('list', 'domainMappings[]', None)
        scope = None
        id = 'id'
        parent_spec = {
            'resource': 'app-engine',
            'child_enum_params': {
                ('id', 'appsId')
            }
        }

        @staticmethod
        def get(client, resource_info):
            apps_id, mapping_id = re.match('apps/(.*?)/domainMappings/(.*)',
                                           resource_info['resourceName']).groups()
            return client.execute_query('get', {'appsId': apps_id,
                                                'domainMappingsId': mapping_id})


@AppEngineDomainMapping.action_registry.register('delete')
class AppEngineDomainMappingDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1
    /apps.domainMappings/delete>`_ an App Engine Domain Mapping.
    The action does not specify any parameters.

    .. code-block:: yaml

        policies:
          - name: gcp-app-engine-domain-mapping-delete
            resource: gcp.app-engine-domain-mapping
            filters:
              - type: value
                key: id
                value: mapping.to.delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        apps_id, mapping_id = re.match('apps/(.*?)/domainMappings/(.*)',
                                       r['name']).groups()
        return {'appsId': apps_id, 'domainMappingsId': mapping_id}


@resources.register('app-engine-firewall-ingress-rule')
class AppEngineFirewallIngressRule(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.firewall.ingressRules
    """
    def _get_parent_resource_info(self, child_instance):
        return {'resourceName': 'apps/%s' %
                                local_session(self.session_factory).get_default_project()}

    class resource_type(ChildTypeInfo):
        service = 'appengine'
        version = 'v1'
        component = 'apps.firewall.ingressRules'
        enum_spec = ('list', 'ingressRules[]', None)
        scope = None
        id = 'priority'
        parent_spec = {
            'resource': 'app-engine',
            'child_enum_params': {
                ('id', 'appsId')
            }
        }

        @staticmethod
        def get(client, resource_info):
            apps_id, ingress_rules_id = re.match('apps/(.*?)/firewall/ingressRules/(.*)',
                                                 resource_info['resourceName']).groups()
            return client.execute_query(
                'get', {'appsId': apps_id,
                        'ingressRulesId': ingress_rules_id})
