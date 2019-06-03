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


@resources.register('bq-datatransfer')
class BigQueryDataTransfer(QueryResourceManager):
    """GCP resource:
    https://cloud.google.com/bigquery/docs/reference/
    datatransfer/rest/v1/projects.locations.transferConfigs/list
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
