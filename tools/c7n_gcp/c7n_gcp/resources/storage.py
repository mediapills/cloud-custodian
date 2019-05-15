# Copyright 2017-2018 Capital One Services, LLC
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

from c7n.utils import local_session
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo


@resources.register('bucket')
class Bucket(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'buckets'
        scope = 'project'
        enum_spec = ('list', 'items[]', {'projection': 'full'})
        id = 'name'
        get_requires_event = True

        @staticmethod
        def get(client, event):
            if 'resource' in event.keys():
                bucket_name = jmespath.search('resource.labels.bucket_name', event)
            else:
                bucket_name = jmespath.search('bucket_name', event)

            return client.execute_command(
                'get', {'bucket': bucket_name})


@resources.register('bucket-access-control')
class BucketAccessControl(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'bucketAccessControls'
        enum_spec = ('list', 'items[]', None)
        id = 'name'
        scope = 'global'
        get_requires_event = True
        parent_spec = {
            'resource': 'bucket',
            'child_enum_params': [
                ('name', 'bucket'),
            ],
            'parent_get_params': [
                ('bucket', 'bucket_name'),
            ]
        }

        @staticmethod
        def get(client, event):
            entity = jmespath.search('protoPayload.serviceData.policyDelta.bindingDeltas[0].member', event)
            if ':' in entity:
                entity = '-'.join(entity.split(':'))
            return client.execute_command(
                'get', {
                    'bucket': jmespath.search('resource.labels.bucket_name', event),
                    'entity': entity
                })


@resources.register('bucket-default-object-access-control')
class DefaultObjectAccessControl(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'defaultObjectAccessControls'
        enum_spec = ('list', 'items[]', None)
        id = 'name'
        scope = 'global'
        parent_spec = {
            'resource': 'bucket',
            'child_enum_params': [
                ('name', 'bucket'),
            ],
            'parent_get_params': [
                ('bucket_name', 'bucket_name'),
            ]
        }

        @staticmethod
        def get(client, resource_info):
            info = client.execute_command(
                'get', {
                    'bucket': resource_info['bucket_name'],
                    'entity': resource_info['entity']
                })
            info['bucket_name'] = resource_info['bucket_name']
            return info


@resources.register('bucket-object')
class BucketObject(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'objects'
        enum_spec = ('list', 'items[]', None)
        id = 'name'
        scope = 'global'
        parent_spec = {
            'resource': 'bucket',
            'child_enum_params': [
                ('name', 'bucket'),
            ],
            'parent_get_params': [
                ('bucket', 'bucket_name'),
            ]
        }

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {
                    'bucket': resource_info['bucket_name'],
                    'object': resource_info['name']
                })


@resources.register('bucket-object-access-control')
class BucketObjectAccessControl(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'objectAccessControls'
        enum_spec = ('list', 'items[]', None)
        id = 'name'
        scope = 'global'
        parent_spec = {
            'resource': 'bucket-object',
            'child_enum_params': [
                ('bucket', 'bucket'),
                ('name', 'object'),
            ],
            'parent_get_params': [
                ('bucket', 'bucket_name'),
                ('object', 'name'),
                ('entity', 'entity'),
            ]
        }

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {
                    'bucket': resource_info['bucket_name'],
                    'object': resource_info['name'],
                    'entity': resource_info['entity']
                })


@resources.register('bucket-notification')
class BucketNotification(ChildResourceManager):
    def _get_parent_resource_info(self, child_instance):
        mappings = {}
        project_param_re = re.compile('.*?/storage/v1/b/(.*?)/notificationConfigs/.*')
        mappings['bucket_name'] = project_param_re.match(child_instance['selfLink']).group(1)
        return mappings

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'notifications'
        enum_spec = ('list', 'items[]', None)
        id = 'id'
        scope = 'global'
        parent_spec = {
            'resource': 'bucket',
            'child_enum_params': [
                ('name', 'bucket'),
            ],
        }

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {
                    'bucket': resource_info['bucket_name'],
                    'notification': resource_info['notification_id']
                })


@resources.register('bucket-service-account')
class BucketServiceAccount(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'projects.serviceAccount'
        scope = None
        enum_spec = ('get', '[@]', None)
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'projectId': resource_info['project_id']})

    def get_resource_query(self):
        return {'projectId': local_session(self.session_factory).get_default_project()}
