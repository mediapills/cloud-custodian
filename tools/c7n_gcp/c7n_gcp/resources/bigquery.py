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

import jmespath
import re

from c7n.utils import type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import (QueryResourceManager, TypeInfo,
                           ChildTypeInfo, ChildResourceManager)


@resources.register('bq-dataset')
class DataSet(QueryResourceManager):
    """GCP resource: https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets
    """
    class resource_type(TypeInfo):
        service = 'bigquery'
        version = 'v2'
        component = 'datasets'
        enum_spec = ('list', 'datasets[]', None)
        scope = 'project'
        scope_key = 'projectId'
        get_requires_event = True
        id = 'id'

        @staticmethod
        def get(client, event):
            # dataset creation doesn't include data set name in resource name.
            if 'protoPayload' in event:
                _, method = event['protoPayload']['methodName'].split('.')
                if method not in ('insert', 'update'):
                    raise RuntimeError('unknown event %s' % event)
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
            dataset_info = client.execute_query(
                'get', verb_arguments=r['datasetReference']
            )

            dataset_info['creationTime'] = float(
                dataset_info['creationTime']
            ) / 1000.0
            dataset_info['lastModifiedTime'] = float(
                dataset_info['lastModifiedTime']
            ) / 1000.0

            results.append(dataset_info)
        return results


@DataSet.action_registry.register('delete')
class DataSetDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/delete>`_ a dataset

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-big-dataset-delete
            resource: gcp.bq-dataset
            filters:
              - type: value
                key: tag:updated
                value: tableexparation
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    path_param_re = re.compile('.*?/projects/(.*?)/datasets/(.*)')

    def get_resource_params(self, model, resource):
        project_id, dataset_id = self.path_param_re.match(
            resource['selfLink']).groups()
        return {
            'projectId': project_id,
            'datasetId': dataset_id,
            'deleteContents': True
        }


@DataSet.action_registry.register('set')
class DataSetSet(MethodAction):
    """
    `Patches <https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch>`_ a dataset

    The `defaultTableExpirationMs` specifies the default lifetime of all tables in the dataset, in
    milliseconds.

    The `labels` specifies the labels associated with this dataset.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-big-dataset-set
            resource: gcp.bq-dataset
            filters:
              - type: value
                key: location
                value: US
            actions:
              - type: set
                defaultTableExpirationMs: 7200000
                labels:
                    updated: tableexparation
    """
    schema = type_schema(
        'set',
        **{
            'defaultTableExpirationMs': {
                'type': 'number',
                'minimum': 3600000
            },
            'labels': {
                'type': 'object',
                'additionalProperties': {'type': 'string'}
            }
        }
    )
    method_spec = {'op': 'patch'}
    path_param_re = re.compile('.*?/projects/(.*?)/datasets/(.*)')

    def get_resource_params(self, model, resource):
        project_id, dataset_id = self.path_param_re.match(
            resource['selfLink']).groups()

        body = {}

        if 'labels' in self.data:
            body['labels'] = self.data['labels']

        if 'defaultTableExpirationMs' in self.data:
            body['defaultTableExpirationMs'] = self.data['defaultTableExpirationMs']

        return {
            'projectId': project_id,
            'datasetId': dataset_id,
            'body': body
        }


@resources.register('bq-job')
class BigQueryJob(QueryResourceManager):
    """GCP resource: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs
    """
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
                    'protoPayload.metadata.tableCreation.jobName', event).rsplit('/', 1)[-1]
            })

    def augment(self, resources):
        update_fields = ['creationTime', 'endTime', 'startTime']
        for r in resources:
            for field in update_fields:
                r['statistics'][field] = float(
                    r['statistics'][field]
                ) / 1000.0
        return resources


@BigQueryJob.action_registry.register('cancel')
class BigQueryJobCancel(MethodAction):
    """
    `Cancels <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel>`_
    a BigQuery job

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-big-jobs-cancel
            resource: gcp.bq-job
            filters:
              - type: value
                key: state
                value: DONE
            actions:
              - type: cancel
    """
    schema = type_schema('cancel')
    method_spec = {'op': 'cancel'}

    def get_resource_params(self, model, resource):
        return resource['jobReference']


@resources.register('bq-project')
class BigQueryProject(QueryResourceManager):
    """GCP resource: https://cloud.google.com/bigquery/docs/reference/rest/v2/projects
    """
    class resource_type(TypeInfo):
        service = 'bigquery'
        version = 'v2'
        component = 'projects'
        enum_spec = ('list', 'projects[]', None)
        scope = 'global'
        id = 'id'


@resources.register('bq-table')
class BigQueryTable(ChildResourceManager):
    """GCP resource: https://cloud.google.com/bigquery/docs/reference/rest/v2/tables
    """
    class resource_type(ChildTypeInfo):
        service = 'bigquery'
        version = 'v2'
        component = 'tables'
        enum_spec = ('list', 'tables[]', None)
        scope_key = 'projectId'
        id = 'id'
        parent_spec = {
            'resource': 'bq-dataset',
            'child_enum_params': [
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
                'projectId': event['project_id'],
                'datasetId': event['dataset_id'],
                'tableId': event['resourceName'].rsplit('/', 1)[-1]
            })

    def augment(self, resources):
        for r in resources:
            r['creationTime'] = float(r['creationTime']) / 1000.0
            if 'expirationTime' in r:
                r['expirationTime'] = float(r['expirationTime']) / 1000.0
        return resources


@BigQueryTable.action_registry.register('delete')
class BigQueryTableDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete>`_
    a BigQuery table

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-big-table-delete
            resource: gcp.bq-table
            filters:
              - type: value
                key: creationTime
                value_type: age
                op: greater-than
                value: 31
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return resource['tableReference']


@BigQueryTable.action_registry.register('set')
class BigQueryTableSet(MethodAction):
    """
    `Patches <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch>`_
    a BigQuery table

    The `expirationTime` specifies the time when this table expires, in milliseconds
    since the epoch.

    The `labels` specifies the labels associated with this table.

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bq-table-delete
            resource: gcp.bq-table
            filters:
              - type: value
                key: expirationTime
                value_type: expiration
                op: less-than
                value: 7
            actions:
              - type: set
                expirationTime: 3600000
                labels:
                    expiration: less_than_seven_days
    """
    schema = type_schema(
        'set',
        **{
            'expirationTime': {
                'type': 'number',
                'minimum': 3600000
            },
            'labels': {
                'type': 'object',
                'additionalProperties': {'type': 'string'}
            }
        }
    )
    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        patch_data = resource['tableReference'].copy()
        body = {}

        if 'labels' in self.data:
            body['labels'] = self.data['labels']

        if 'expirationTime' in self.data:
            body['expirationTime'] = self.data['expirationTime']

        patch_data.update({'body': body})
        return patch_data
