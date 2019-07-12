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


class AppEnginePatchServingStatusAction(MethodAction):
    """
    `Patches <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps/patch>`_
    the 'Serving' setting. Is supposed to be extended to call `_get_resource_params`
    from the original `get_resource_params` method with the `serving` flag provided
    which sets 'servingStatus' either to 'SERVING' or 'USER_DISABLED'.

    Apart from that, `schema` is also expected to be specified in subclasses.
    """
    method_spec = {'op': 'patch'}

    def _get_resource_params(self, r, serving):
        serving_status = 'SERVING' if serving else 'USER_DISABLED'
        return {'appsId': r['id'],
                'body': {'servingStatus': serving_status},
                'updateMask': 'serving_status'}


@AppEngineApp.action_registry.register('start')
class AppEngineStart(AppEnginePatchServingStatusAction):
    """
    Starts App Engine by extending `AppEnginePatchServingStatusAction`

    .. code-block:: yaml

        policies:
          - name: gcp-app-engine-start
            resource: gcp.app-engine
            actions:
              - type: start
    """
    schema = type_schema('start')

    def get_resource_params(self, m, r):
        return AppEnginePatchServingStatusAction._get_resource_params(self, r, True)


@AppEngineApp.action_registry.register('stop')
class AppEngineStop(AppEnginePatchServingStatusAction):
    """
    Stops App Engine by extending `AppEnginePatchServingStatusAction`

    .. code-block:: yaml

        policies:
          - name: gcp-app-engine-stop
            resource: gcp.app-engine
            actions:
              - type: stop
    """
    schema = type_schema('stop')

    def get_resource_params(self, m, r):
        return AppEnginePatchServingStatusAction._get_resource_params(self, r, False)


@AppEngineApp.action_registry.register('set')
class AppEnginePatchSettings(MethodAction):
    """
    `Patches <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps/patch>`_
    the 'Split health checks' and 'Use Container-Optimized OS' settings.

    If a setting is disabled, the key is removed from the resource rather than
    being marked as `false`.

    The 'split-health-check' flag controls if split health checks ('readinessCheck'
    and 'livenessCheck' at an app.yaml level) should be used instead of the legacy
    health checks ('healthCheck')

    The 'use-container-optimised-os' flag enables the use if Container-Optimized OS
    base image for VMs, rather than a base Debian image. Before patching the setting,
    make sure it is enabled for your project, otherwise the update `operation
    <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.operations/list>`_
    will fail although the policy will show no errors.

    .. code-block:: yaml

        policies:
          - name: gcp-app-engine-set
            resource: gcp.app-engine
            actions:
              - type: set
                split-health-checks: true
                use-container-optimized-os: true
    """
    schema = type_schema('set',
                         **{
                             'additionalProperties': False,
                             'split-health-checks': {'type': 'boolean'},
                             'use-container-optimized-os': {'type': 'boolean'}
                         })
    method_spec = {'op': 'patch'}

    def get_resource_params(self, m, r):
        params = {'appsId': r['id'],
                  'body': {'featureSettings': {}},
                  'updateMask': 'featureSettings'}
        feature_settings = params['body']['featureSettings']
        if 'split-health-checks' in self.data:
            feature_settings['splitHealthChecks'] = self.data['split-health-checks']
        if 'use-container-optimized-os' in self.data:
            feature_settings['useContainerOptimizedOs'] = self.data['use-container-optimized-os']
        return params


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
