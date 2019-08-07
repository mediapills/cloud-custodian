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
import json
from c7n.utils import type_schema, local_session
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo
from c7n_gcp.actions import MethodAction


@resources.register('storagetransfer-transfer-job')
class StorageTransferTransferJob(QueryResourceManager):
    """GCP resource:
    https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferJobs
    """

    class resource_type(TypeInfo):
        service = 'storagetransfer'
        version = 'v1'
        component = 'transferJobs'
        scope = 'global'
        enum_spec = ('list', 'transferJobs[]', None)
        id = 'name'

    def get_resource_query(self):
        return {'filter': {
            'project_id': local_session(self.session_factory).get_default_project()
        }}


@StorageTransferTransferJob.action_registry.register('set')
class StorageTransferTransferJobSet(MethodAction):
    """The action is used for Storage Transfer service transferJobs patch.

    GCP actions is
    https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferJobs/patch

    Example:

    .. code-block:: yaml

        policies:
          - name: storage-transfer-transfer-job-set-and-notify
            resource: gcp.storagetransfer-transfer-job
            filters:
              - type: value
                key: creationTime
                op: greater-than
                value_type: age
                value: 365
            actions:
              - type: set
                status: DISABLED
              - type: notify
                to:
                  - email@address
                format: json
                transport:
                  type: pubsub
                  topic: projects/cloud-custodian/topics/storage-transfer
    """

    schema = type_schema('set',
         **{'status': {'type': 'string'},
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            })

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        project = local_session(self.manager.source.query.session_factory).get_default_project()
        body = {
            'transferJob': {},
            'projectId': project
        }

        for field in ['status', 'name', 'description']:
            if field in self.data:
                body['transferJob'][field] = self.data[field]

        return {
            'jobName': resource['name'],
            'body': body}
