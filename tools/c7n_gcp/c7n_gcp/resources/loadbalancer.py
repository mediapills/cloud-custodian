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
from c7n.utils import type_schema, local_session
from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo


@resources.register('loadbalancer-address')
class LoadBalancingAddress(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/addresses
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'addresses'
        enum_spec = ('aggregatedList', 'items.*.addresses[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['location'],
                'address': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-url-map')
class LoadBalancingUrlMap(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/urlMaps
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'urlMaps'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'urlMap': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-target-tcp-proxy')
class LoadBalancingTargetTcpProxy(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/targetTcpProxies
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'targetTcpProxies'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'targetTcpProxy': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-target-ssl-proxy')
class LoadBalancingTargetSslProxy(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/targetSslProxies
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'targetSslProxies'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'targetSslProxy': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-ssl-policy')
class LoadBalancingSslPolicy(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/sslPolicies
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'sslPolicies'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'sslPolicy': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@LoadBalancingSslPolicy.action_registry.register('delete')
class LoadBalancingSslPolicyDelete(MethodAction):
    """The action is used for Load Balancing SSL Policies delete.
    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/sslPolicies/delete.

    Example:

    .. code-block:: yaml

        policies:
          - name: gcp-load-balancing-ssl-policies-delete
            resource: gcp.loadbalancer-ssl-policy
            filters:
              - type: value
                key: minTlsVersion
                op: ne
                value: TLS_1_2
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        return {
            'project': project,
            'sslPolicy': resource['name']}


@resources.register('loadbalancer-ssl-certificate')
class LoadBalancingSslCertificate(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/sslCertificates
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'sslCertificates'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'sslCertificate': resource_info['ssl_certificate_name']})


@resources.register('loadbalancer-target-https-proxy')
class LoadBalancingTargetHttpsProxy(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/targetHttpsProxies
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'targetHttpsProxies'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'targetHttpsProxy': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-backend-bucket')
class LoadBalancingBackendBucket(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/backendBuckets
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'backendBuckets'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'backendBucket': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@LoadBalancingBackendBucket.action_registry.register('delete')
class LoadBalancingBackendBucketDelete(MethodAction):
    """The action is used for Load Balancing Backend Buckets delete.
    
    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/backendBuckets/delete.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-loadbalancer-backend-buckets-delete
            resource: gcp.loadbalancer-backend-bucket
            filters:
              - type: value
                key: bucketName
                op: eq
                value: custodian-bucket-0
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        return {
            'project': project,
            'backendBucket': resource['name']}


@resources.register('loadbalancer-https-health-check')
class LoadBalancingHttpsHealthCheck(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/httpsHealthChecks
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'httpsHealthChecks'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'httpsHealthCheck': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@LoadBalancingHttpsHealthCheck.action_registry.register('delete')
class LoadBalancingHttpsHealthCheckDelete(MethodAction):
    """The action is used for Load Balancing HTTPs Health Checks delete.

    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/httpsHealthChecks/delete.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-loadbalancer-delete-https-health-checks
            resource: gcp.loadbalancer-https-health-check
            filters:
              - type: value
                key: host
                op: contains
                value: dev-
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        return {
            'project': project,
            'httpsHealthCheck': resource['name']}


@LoadBalancingHttpsHealthCheck.action_registry.register('set')
class LoadBalancingHttpsHealthCheckPatch(MethodAction):
    """The action is used for Load Balancing HTTPs Health Checks patch.

    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/httpsHealthChecks/patch.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-loadbalancer-update-https-health-checks
            resource: gcp.loadbalancer-https-health-check
            filters:
              - type: value
                key: host
                op: eq
                value: custodian.com
            actions:
              - type: set
                healthyThreshold: 2
                host: cloudcustodian.com
                requestPath: /test
                port: 8080
                checkIntervalSec: 10
                timeoutSec: 9
                unhealthyThreshold: 10
    """
    schema = type_schema('set',
                         **{'host': {'type': 'string'},
                            'requestPath': {'type': 'string'},
                            'port': {'type': 'integer'},
                            'checkIntervalSec': {'type': 'integer'},
                            'timeoutSec': {'type': 'integer'},
                            'unhealthyThreshold': {'type': 'integer'},
                            'healthyThreshold': {'type': 'integer'}
                            })
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        body = {}
        for field in self.data:
            if field != 'name' and field != 'type':
                body[field] = self.data[field]

        return {
            'project': project,
            'httpsHealthCheck': resource['name'],
            'body': body}


@resources.register('loadbalancer-http-health-check')
class LoadBalancingHttpHealthCheck(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/httpHealthChecks
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'httpHealthChecks'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'httpHealthCheck': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@LoadBalancingHttpHealthCheck.action_registry.register('delete')
class LoadBalancingHttpHealthCheckDelete(MethodAction):
    """The action is used for Load Balancing HTTP Health Checks delete.

    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/httpHealthChecks/delete.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-loadbalancer-delete-http-health-checks
            resource: gcp.loadbalancer-http-health-check
            filters:
              - type: value
                key: host
                op: contains
                value: dev-
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        return {
            'project': project,
            'httpHealthCheck': resource['name']}


@LoadBalancingHttpHealthCheck.action_registry.register('set')
class LoadBalancingHttpHealthCheckPatch(MethodAction):
    """The action is used for Load Balancing HTTP Health Checks patch.

    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/httpHealthChecks/patch.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-loadbalancer-update-http-health-checks
            resource: gcp.loadbalancer-http-health-check
            filters:
              - type: value
                key: host
                op: eq
                value: custodian.com
            actions:
              - type: set
                healthyThreshold: 2
                host: cloudcustodian.com
                requestPath: /test
                port: 8080
                checkIntervalSec: 10
                timeoutSec: 9
                unhealthyThreshold: 10
    """
    schema = type_schema('set',
                         **{'host': {'type': 'string'},
                            'requestPath': {'type': 'string'},
                            'port': {'type': 'integer'},
                            'checkIntervalSec': {'type': 'integer'},
                            'timeoutSec': {'type': 'integer'},
                            'unhealthyThreshold': {'type': 'integer'},
                            'healthyThreshold': {'type': 'integer'}
                            })
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        body = {}
        for field in self.data:
            if field != 'name' and field != 'type':
                body[field] = self.data[field]

        return {
            'project': project,
            'httpHealthCheck': resource['name'],
            'body': body}


@resources.register('loadbalancer-health-check')
class LoadBalancingHealthCheck(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/healthChecks
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'healthChecks'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'healthCheck': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@LoadBalancingHealthCheck.action_registry.register('delete')
class LoadBalancingHealthCheckDelete(MethodAction):
    """The action is used for Load Balancing Health Checks delete.
    
    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/healthChecks/delete.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-loadbalancer-delete-health-checks
            resource: gcp.loadbalancer-health-check
            filters:
              - type: value
                key: httpHealthCheck.host
                op: contains
                value: -dev-
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        return {
            'project': project,
            'healthCheck': resource['name']}


@LoadBalancingHealthCheck.action_registry.register('set')
class LoadBalancingHealthCheckPatch(MethodAction):
    """The action is used for Load Balancing Health Checks patch.

    GCP action is https://cloud.google.com/compute/docs/reference/rest/v1/healthChecks/patch.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-loadbalancer-update-health-checks
            resource: gcp.loadbalancer-health-check
            filters:
              - type: value
                key: httpHealthCheck.host
                op: contains
                value: -dev-
            actions:
              - type: set
                httpHealthCheck:
                  host: cloudcustodian.com
                  requestPath: /test
                  port: 8080
                healthyThreshold: 2
                checkIntervalSec: 10
                timeoutSec: 9
                unhealthyThreshold: 10
    """
    health_check_type = {
        'type': 'object',
        'host': {'type': 'string'},
        'requestPath': {'type': 'string'},
        'port': {'type': 'integer'},
    }

    schema = type_schema('set',
                         **{'tcpHealthCheck': health_check_type,
                            'sslHealthCheck': health_check_type,
                            'httpHealthCheck': health_check_type,
                            'httpsHealthCheck': health_check_type,
                            'http2HealthCheck': health_check_type,
                            'checkIntervalSec': {'type': 'integer'},
                            'timeoutSec': {'type': 'integer'},
                            'unhealthyThreshold': {'type': 'integer'},
                            'healthyThreshold': {'type': 'integer'}
                            })
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        body = {}
        for field in self.data:
            if field != 'name' and field != 'type':
                body[field] = self.data[field]

        return {
            'project': project,
            'healthCheck': resource['name'],
            'body': body}


@resources.register('loadbalancer-target-http-proxy')
class LoadBalancingTargetHttpProxy(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/targetHttpProxies
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'targetHttpProxies'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'targetHttpProxy': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-backend-service')
class LoadBalancingBackendService(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/backendServices
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'backendServices'
        enum_spec = ('aggregatedList', 'items.*.backendServices[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'backendService': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-target-instance')
class LoadBalancingTargetInstance(QueryResourceManager):
    """    GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/targetInstances
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'targetInstances'
        enum_spec = ('aggregatedList', 'items.*.targetInstances[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'zone': resource_info['zone'],
                'targetInstance': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-target-pool')
class LoadBalancingTargetPool(QueryResourceManager):
    """    GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/targetPools
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'targetPools'
        enum_spec = ('aggregatedList', 'items.*.targetPools[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['zone'],
                'targetPool': resource_info[
                    'resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-forwarding-rule')
class LoadBalancingForwardingRule(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/addresses
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'forwardingRules'
        enum_spec = ('aggregatedList', 'items.*.forwardingRules[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'region': resource_info['region'],
                'forwardingRule': resource_info['resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-global-forwarding-rule')
class LoadBalancingGlobalForwardingRule(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/forwardingRules
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'globalForwardingRules'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'forwardingRule': resource_info['resourceName'].rsplit('/', 1)[-1]})


@resources.register('loadbalancer-global-address')
class LoadBalancingGlobalAddress(QueryResourceManager):
    """GCP resource: https://cloud.google.com/compute/docs/reference/rest/v1/globalAddresses
    """
    class resource_type(TypeInfo):
        service = 'compute'
        version = 'v1'
        component = 'globalAddresses'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command('get', {
                'project': resource_info['project_id'],
                'address': resource_info['resourceName'].rsplit('/', 1)[-1]})
