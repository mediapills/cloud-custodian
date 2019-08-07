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
from c7n_gcp.query import QueryResourceManager, TypeInfo
from c7n_gcp.provider import resources
from c7n.utils import type_schema
from c7n_gcp.actions import MethodAction


@resources.register('bq-datatransfer-transfer-config')
class BigQueryDataTransferConfig(QueryResourceManager):
    """GCP resource: https://cloud.google.com/bigquery/docs/reference/
    datatransfer/rest/v1/projects.locations.transferConfigs
    """

    class resource_type(TypeInfo):
        service = 'bigquerydatatransfer'
        version = 'v1'
        component = 'projects.transferConfigs'
        enum_spec = ('list', 'transferConfigs[]', None)
        scope = 'project'
        scope_key = 'parent'
        scope_template = 'projects/{}'
        id = 'id'


@BigQueryDataTransferConfig.action_registry.register('delete')
class BigQueryDataTransferConfigDelete(MethodAction):
    """The action is used for BigQueryData projects.locations.transferConfigs delete.
    
    GCP action is
    https://cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/delete

    :Example:

    .. code-block:: yaml

        policies:
          - name: bq-datatransfer-transfer-config-delete-failed
            resource: gcp.bq-datatransfer-transfer-config
            filters:
              - type: value
                key: state
                value: FAILED
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        name = resource["name"].split('/')
        del name[2:4]
        return {'name': '/'.join(name)}
