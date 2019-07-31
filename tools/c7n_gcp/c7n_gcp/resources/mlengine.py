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
import jmespath

from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo
from c7n_gcp.actions import MethodAction
from c7n.utils import type_schema, local_session


@resources.register('ml-model')
class MLModel(QueryResourceManager):
    """The action is used for ML projects.models get and list actions.

    GCP action is https://cloud.google.com/ml-engine/reference/rest/v1/projects.models

    Example:

    .. code-block:: yaml

        policies:
          - name: ml-model-list
            resource: gcp.ml-model
            filters:
              - type: value
                key: name
                value: projects/cloud-custodian/models/test
    """

    class resource_type(TypeInfo):
        service = 'ml'
        version = 'v1'
        component = 'projects.models'
        enum_spec = ('list', 'models[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'
        get_requires_event = True

        @staticmethod
        def get(client, event):
            return client.execute_query(
                'get', {'name': jmespath.search(
                    'protoPayload.response.name', event
                )})


@MLModel.action_registry.register('set')
class MLModelActionPatch(MethodAction):
    """The action is used for ML projects.models update description.

    GCP action is https://cloud.google.com/ml-engine/reference/rest/v1/projects.models/patch

    Example:

    .. code-block:: yaml

        policies:
          - name: ml-model-update-description
            resource: gcp.ml-model
            filters:
              - type: value
                key: name
                value: projects/cloud-custodian/models/test
            actions:
              - type: set
                description: Custom description
    """

    schema = type_schema(
        'set',
        **{
            'description': {
                'type': 'string'
            }
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):

        return {
            'name': resource['name'],
            'updateMask': 'description',
            'body': {
                'description': self.data['description']
            }}


@MLModel.action_registry.register('delete')
class MLModelActionDelete(MethodAction):
    """The action is used for ML projects.models delete model.

    GCP action is https://cloud.google.com/ml-engine/reference/rest/v1/projects.models/delete

    Example:

    .. code-block:: yaml

        policies:
          - name: ml-model-delete
            resource: gcp.ml-model
            filters:
              - type: value
                key: name
                value: projects/cloud-custodian/models/test
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'name': resource['name']}


@resources.register('ml-job')
class MLJob(QueryResourceManager):
    """The action is used for ML projects.jobs list and get actions.

    GCP action is https://cloud.google.com/ml-engine/reference/rest/v1/projects.jobs

    Example:

    .. code-block:: yaml

        policies:
          - name: ml-job-set-labels
            resource: gcp.ml-job
            filters:
              - type: value
                key: jobId
                value: test_job
    """

    class resource_type(TypeInfo):
        service = 'ml'
        version = 'v1'
        component = 'projects.jobs'
        enum_spec = ('list', 'jobs[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'name'
        get_requires_event = True

        @staticmethod
        def get(client, event):
            return client.execute_query(
                'get', {'name': 'projects/{}/jobs/{}'.format(
                    jmespath.search('resource.labels.project_id', event),
                    jmespath.search('protoPayload.response.jobId', event))})


@MLJob.action_registry.register('set')
class MLJobActionPatch(MethodAction):
    """The action is used for ML projects.jobs set labels.

    GCP action is https://cloud.google.com/ml-engine/reference/rest/v1/projects.jobs/patch

    Example:

    .. code-block:: yaml

        policies:
          - name: ml-job-set-labels
            resource: gcp.ml-job
            filters:
              - type: value
                key: jobId
                value: test_job
            actions:
              - type: set-labels
                labels:
                  - key: type
                    value: new
    """

    schema = type_schema(
        'set',
        **{
            'labels': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'key': {'type': 'string'},
                        'value': {'type': 'string'}
                    }
                }
            }
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        session = local_session(self.manager.session_factory)
        name = 'projects/{}/jobs/{}'.format(
            session.get_default_project(),
            resource['jobId'])

        return {
            'name': name,
            'updateMask': 'labels',
            'body': {
                'labels': {
                    label['key']: label['value'] for label in self.data['labels']
                }
            }}
