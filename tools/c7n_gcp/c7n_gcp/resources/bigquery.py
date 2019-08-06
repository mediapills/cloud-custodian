# Copyright 2018 Capital One Services, LLC
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

import jmespath
from c7n.utils import type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildTypeInfo, ChildResourceManager
from c7n_gcp.provider import resources


@resources.register('bq-dataset')
class DataSet(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'bigquery'
        version = 'v2'
        component = 'datasets'
        enum_spec = ('list', 'datasets[]', None)
        scope = 'project'
        scope_key = 'projectId'
        get_requires_event = True
        id = "id"

        @staticmethod
        def get(client, event):
            # dataset creation doesn't include data set name in resource name.
            if 'protoPayload' in event:
                _, method = event['protoPayload']['methodName'].split('.')
                if method not in ('insert', 'update'):
                    raise RuntimeError("unknown event %s" % event)
                expr = 'protoPayload.serviceData.dataset{}Response.resource.datasetName'.format(
                    method.capitalize())
                ref = jmespath.search(expr, event)
            else:
                ref = event
            return client.execute_query('get', verb_arguments=ref)

    def augment(self, resources):
        client = self.get_client()
        results = []
        for r in resources:
            ref = r['datasetReference']
            results.append(
                client.execute_query(
                    'get', verb_arguments=ref))
        return results


@DataSet.action_registry.register('delete')
class DataSetDelete(MethodAction):
    """The action is used for bigquery datasets delete.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/delete

    :Example:

    .. code-block:: yaml

          policies:
            - name: gcp-big-dataset-delete
              resource: gcp.bq-dataset
              filters:
                - type: value
                  key: id
                  value: project_id:dataset_id
              actions:
                - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/datasets/(.*)')

    def get_resource_params(self, model, resource):
        project_id, dataset_id = self.path_param_re.match(
            resource['selfLink']).groups()
        return {
            'projectId': project_id,
            'datasetId': dataset_id,
            'deleteContents': True
        }


@DataSet.action_registry.register('set-table-expiration')
class DataSetSet(MethodAction):
    """The action is used for bigquery datasets patch.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-big-dataset-update-table-expiration
            resource: gcp.bq-dataset
            filters:
              - type: value
                key: id
                value: project_id:dataset_id
            actions:
              - type: set-table-expiration
                tableExpirationMs: 7200000
    """

    schema = type_schema(
        'set-table-expiration',
        **{
            'type': {'enum': ['set-table-expiration']},
            'tableExpirationMs': {
                'type': 'number',
                'minimum': 3600000
            }
        }
    )

    method_spec = {'op': 'patch'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/datasets/(.*)')

    def get_resource_params(self, model, resource):
        project_id, dataset_id = self.path_param_re.match(
            resource['selfLink']).groups()
        return {
            'projectId': project_id,
            'datasetId': dataset_id,
            'body': {'defaultTableExpirationMs': self.data['tableExpirationMs']}
        }


@resources.register('bq-job')
class BigQueryJob(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'bigquery'
        version = 'v2'
        component = 'jobs'
        enum_spec = ('list', 'jobs[]', {'allUsers': True})
        get_requires_event = True
        scope = 'project'
        scope_key = 'projectId'
        id = 'id'

        @staticmethod
        def get(client, event):
            return client.execute_query('get', {
                'projectId': jmespath.search('resource.labels.project_id', event),
                'jobId': jmespath.search(
                    'protoPayload.metadata.tableCreation.jobName', event
                ).rsplit('/', 1)[-1]
            })


@BigQueryJob.action_registry.register('cancel')
class BigQueryJobCancel(MethodAction):
    """The action is used for bigquery jobs cancel.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-big-jobs-cancel
            resource: gcp.bq-job
            filters:
              - type: value
                key: jobReference.jobId
                value: jobId
            actions:
              - type: cancel
    """
    schema = type_schema('cancel')
    method_spec = {'op': 'cancel'}

    def get_resource_params(self, model, resource):
        return resource['jobReference']


@resources.register('bq-project')
class BigQueryProject(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'bigquery'
        version = 'v2'
        component = 'projects'
        enum_spec = ('list', 'projects[]', None)
        scope = 'global'
        id = 'id'


@resources.register('bq-table')
class BigQueryTable(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'bigquery'
        version = 'v2'
        component = 'tables'
        enum_spec = ('list', 'tables[]', None)
        scope = 'global'
        id = 'id'
        get_requires_event = True
        parent_spec = {
            'resource': 'bq-dataset',
            'child_enum_params': [
                ('datasetReference.projectId', 'projectId'),
                ('datasetReference.datasetId', 'datasetId'),
            ],
            'parent_get_params': [
                ('tableReference.projectId', 'projectId'),
                ('tableReference.datasetId', 'datasetId'),
            ]
        }

        @staticmethod
        def get(client, event):
            return client.execute_query('get', {
                'projectId': jmespath.search('resource.labels.project_id', event),
                'datasetId': jmespath.search('resource.labels.dataset_id', event),
                'tableId': jmespath.search('protoPayload.resourceName', event).rsplit('/', 1)[-1]
            })
