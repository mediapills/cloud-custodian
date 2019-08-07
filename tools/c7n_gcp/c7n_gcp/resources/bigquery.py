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
from c7n_gcp.query import (QueryResourceManager, TypeInfo,
                           ChildTypeInfo, ChildResourceManager)
from c7n_gcp.provider import resources


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
    """The action is used for bigquery datasets delete.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/delete

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


@DataSet.action_registry.register('set')
class DataSetSet(MethodAction):
    """The action is used for bigquery datasets patch.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch

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
                tableExpirationMs: 7200000
                labels:
                  - key: updated
                    value: tableexparation
    """

    schema = type_schema(
        'set',
        **{
            'tableExpirationMs': {
                'type': 'number',
                'minimum': 3600000
            },
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
    path_param_re = re.compile(
        '.*?/projects/(.*?)/datasets/(.*)')

    def get_resource_params(self, model, resource):
        project_id, dataset_id = self.path_param_re.match(
            resource['selfLink']).groups()

        body = {}

        if 'labels' in self.data:
            body.update({'labels': {
                label['key']: label['value'] for label in
                self.data['labels']
            }})
        if 'tableExpirationMs' in self.data:
            body.update({
                'defaultTableExpirationMs': self.data['tableExpirationMs']
            })

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
                'projectId': jmespath.search('resource.labels.project_id',
                                             event),
                'jobId': jmespath.search(
                    'protoPayload.metadata.tableCreation.jobName', event
                ).rsplit('/', 1)[-1]
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
    """The action is used for bigquery jobs cancel.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel

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
    """The action is used for bigquery table delete.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-big-table-delete
            resource: gcp.bq-table
            filters:
              - type: value
                key: creationTime
                value_type: age
                op: greater-then
                value: 31
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return resource['tableReference']


@BigQueryTable.action_registry.register('set')
class BigQueryTablePatch(MethodAction):
    """The action is used for bigquery table labels patch.

    GCP action is https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch

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
                  - key: expiration
                    value: less_than_seven_days
    """

    schema = type_schema(
        'set',
        **{
            'expirationTime': {
                'type': 'number',
                'minimum': 3600000
            },
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
        patch_data = resource['tableReference'].copy()
        body = {}

        if 'labels' in self.data:
            body.update({'labels': {
                label['key']: label['value'] for label in
                self.data['labels']
            }})

        if 'expirationTime' in self.data:
            body.update({
                'expirationTime': self.data['expirationTime']
            })

        patch_data.update({'body': body})
        return patch_data
