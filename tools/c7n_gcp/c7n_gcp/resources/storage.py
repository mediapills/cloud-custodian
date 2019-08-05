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

import jmespath
from c7n.utils import type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo


@resources.register('bucket')
class Bucket(QueryResourceManager):
    """GCP resource: https://cloud.google.com/storage/docs/json_api/v1/buckets
    """
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
            if 'resource' in event:
                bucket_name = jmespath.search('resource.labels.bucket_name', event)
            else:
                bucket_name = jmespath.search('bucket_name', event)

            return client.execute_command(
                'get', {'bucket': bucket_name})


@Bucket.action_registry.register('delete')
class BucketDelete(MethodAction):
    """The action is used for Bucket delete.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/buckets/delete

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-delete
            resource: gcp.bucket
            filters:
              - type: value
                key: updated
                op: greater-than
                value_type: age
                value: 365
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {'bucket': resource['id']}


@Bucket.action_registry.register('set')
class BucketSet(MethodAction):
    """The action is used for Bucket storage-class patch.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/buckets/patch

    Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-update-storage-class
            resource: gcp.bucket
            filters:
              - type: value
                key: location
                value: US
            actions:
              - type: set
                class: MULTI_REGIONAL
    """

    schema = type_schema(
        'set',
        **{
            'class': {
                'type': 'string',
                'enum': [
                    "MULTI_REGIONAL", "REGIONAL", "STANDARD",
                    "NEARLINE", "COLDLINE", "DURABLE_REDUCED_AVAILABILITY"
                ]
            }
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'bucket': resource['id'],
            'body': {'storageClass': self.data['class']}
        }


@resources.register('bucket-access-control')
class BucketAccessControl(ChildResourceManager):
    """GCP resource: https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls
    """
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


@BucketAccessControl.action_registry.register('set')
class BucketAccessControlSet(MethodAction):
    """The action is used for BucketAccessControl role update.
    
    GCP action is https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls/patch

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-access-control-update-role
            resource: gcp.bucket-access-control
            filters:
              - type: value
                key: entity
                value: entity_name
            actions:
              - type: set
                role: OWNER
    """

    schema = type_schema(
        'set',
        **{
            'role': {'type': 'string'}
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'bucket': resource['bucket'],
            'entity': resource['entity'],
            'body': {'role': self.data['role']}
        }


@BucketAccessControl.action_registry.register('delete')
class BucketAccessControlDelete(MethodAction):
    """The action is used for Bucket delete.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls/delete

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-access-control-delete-role
            resource: gcp.bucket-access-control
            filters:
              - type: value
                key: role
                value: READER
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {
            'bucket': resource['bucket'],
            'entity': resource['entity']
        }


@resources.register('bucket-default-object-access-control')
class BucketDefaultObjectAccessControl(ChildResourceManager):
    """GCP resource: https://cloud.google.com/storage/docs/json_api/v1/defaultObjectAccessControls
    """

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'defaultObjectAccessControls'
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
                ('bucket_name', 'bucket_name'),
            ]
        }

        @staticmethod
        def get(client, event):
            entity = jmespath.search(
                'protoPayload.request.defaultObjectAcl.bindings[0].members[-1]',
                event
            )
            bucket_name = jmespath.search('resource.labels.bucket_name', event)
            if ':' in entity:
                entity = '-'.join(entity.split(':'))

            info = client.execute_command(
                'get', {
                    'bucket': bucket_name,
                    'entity': entity
                })
            info['bucket_name'] = bucket_name
            return info


@BucketDefaultObjectAccessControl.action_registry.register('set')
class BucketDefaultObjectAccessControlSet(MethodAction):
    """The action is used for BucketDefaultObjectAccessControl role update.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/defaultObjectAccessControls
    /patch

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-default-object-access-control-set-role
            resource: gcp.bucket-default-object-access-control
            filters:
              - type: value
                key: entity
                value: entity_name
            actions:
              - type: set
                role: OWNER
    """

    schema = type_schema(
        'set',
        **{
            'role': {'type': 'string'}
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        key = self.manager.resource_type.get_parent_annotation_key()

        return {
            'bucket': resource[key]['name'],
            'entity': resource['entity'],
            'body': {'role': self.data['role']}
        }


@BucketDefaultObjectAccessControl.action_registry.register('delete')
class BucketDefaultObjectAccessControlDelete(MethodAction):
    """The action is used for BucketDefaultObjectAccessControlDelete delete.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/defaultObjectAccessControls
    /delete

    Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-default-object-access-control-role
            resource: gcp.bucket-default-object-access-control
            filters:
              - type: value
                key: entity
                value: entity_name
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        key = self.manager.resource_type.get_parent_annotation_key()

        return {
            'bucket': resource[key]['name'],
            'entity': resource['entity']
        }


@resources.register('bucket-object')
class BucketObject(ChildResourceManager):
    """GCP resource: https://cloud.google.com/storage/docs/json_api/v1/objects
    """

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'objects'
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
            if 'protoPayload' in event:
                bucket_name = jmespath.search('resource.labels.bucket_name', event)
                object_name = jmespath.search('protoPayload.resourceName', event).split('/')[-1]
            else:
                bucket_name = event['bucket_name']
                object_name = event['name']

            return client.execute_command(
                'get', {
                    'bucket': bucket_name,
                    'object': object_name
                })


@BucketObject.action_registry.register('set')
class BucketObjectSet(MethodAction):
    """The action is used for BucketObject cache control patch.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/objects/patch

    Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-object-update-content-type
            resource: gcp.bucket-object
            filters:
              - type: value
                key: updated
                op: greater-than
                value_type: age
                value: 365
            actions:
              - type: set
                cache_control: max-age=3600
    """

    schema = type_schema(
        'set',
        **{
            'cache_control': {'type': 'string'}
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'bucket': resource['bucket'],
            'object': resource['name'],
            'body': {'cacheControl': self.data['cache_control']}
        }


@BucketObject.action_registry.register('delete')
class BucketObjectDelete(MethodAction):
    """The action is used for BucketObject delete.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/objects/delete

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-object-delete
            resource: gcp.bucket-object
            filters:
              - type: value
                key: timeCreated
                op: greater-than
                value_type: age
                value: 365
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {
            'bucket': resource['bucket'],
            'object': resource['name']
        }


@resources.register('bucket-object-access-control')
class BucketObjectAccessControl(ChildResourceManager):
    """GCP resource: https://cloud.google.com/storage/docs/json_api/v1/objectAccessControls
    """

    class resource_type(ChildTypeInfo):
        service = 'storage'
        version = 'v1'
        component = 'objectAccessControls'
        enum_spec = ('list', 'items[]', None)
        id = 'name'
        scope = 'global'
        get_requires_event = True
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
        def get(client, event):
            entity = jmespath.search(
                'protoPayload.serviceData.policyDelta.bindingDeltas[0].member',
                event
            )
            bucket_name = jmespath.search('resource.labels.bucket_name', event)
            object_name = jmespath.search('protoPayload.resourceName', event).split('/')[-1]

            if ':' in entity:
                entity = '-'.join(entity.split(':'))

            return client.execute_command(
                'get', {
                    'bucket': bucket_name,
                    'object': object_name,
                    'entity': entity
                })


@BucketObjectAccessControl.action_registry.register('set')
class BucketObjectAccessControlSet(MethodAction):
    """The action is used for BucketObjectAccessControl role patch.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/objectAccessControls/patch

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-object-access-control-set-role
            resource: gcp.bucket-object-access-control
            filters:
              - type: value
                key: entity
                value: entity_name
            actions:
              - type: set
                role: OWNER
    """

    schema = type_schema(
        'set',
        **{
            'role': {'type': 'string'}
        }
    )

    method_spec = {'op': 'patch'}

    def get_resource_params(self, model, resource):
        return {
            'bucket': resource['bucket'],
            'object': resource['object'],
            'entity': resource['entity'],
            'body': {'role': self.data['role']}
        }


@BucketObjectAccessControl.action_registry.register('delete')
class BucketObjectAccessControlDelete(MethodAction):
    """The action is used for BucketObjectAccessControl delete.

    GCP action is https://cloud.google.com/storage/docs/json_api/v1/objectAccessControls/delete

    :Example:

    .. code-block:: yaml

        policies:
          - name: gcp-bucket-object-access-control-role
            resource: gcp.bucket-object-access-control
            filters:
              - type: value
                key: entity
                value: entity_name
            actions:
              - type: delete
    """

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, model, resource):
        return {
            'bucket': resource['bucket'],
            'object': resource['object'],
            'entity': resource['entity']
        }
