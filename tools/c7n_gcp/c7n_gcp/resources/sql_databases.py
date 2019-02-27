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

from c7n.utils import type_schema
from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo


@resources.register('sql-instance-database')
class SqlInstanceDatabase(QueryResourceManager):
    """https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/databases/list"""
    class resource_type(TypeInfo):
        service = 'sqladmin'
        version = 'v1beta4'
        component = 'databases'
        enum_spec = ('list', "items[]", None)
        scope = 'project'

    def get_resource_query(self):
        if 'query' in self.data:
            return self.data.get('query')[0]


class SqlInstanceDatabaseAction(MethodAction):
    path_param_re = re.compile('.*?/projects/(.*?)/instances/(.*)/databases/(.*)')

    def get_resource_params(self, model, resource):
        project, instance, database = self.path_param_re.match(
            resource['selfLink']).groups()
        return {
            'project': project,
            'instance': instance,
            'database': database
        }
