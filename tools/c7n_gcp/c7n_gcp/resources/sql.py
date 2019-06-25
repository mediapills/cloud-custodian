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
from c7n_gcp.query import (
    QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo
)
from datetime import datetime
from dateutil.parser import parse


@resources.register('sql-instance')
class SqlInstance(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'sqladmin'
        version = 'v1beta4'
        component = 'instances'
        enum_spec = ('list', 'items[]', None)
        scope = 'project'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'project': resource_info['project_id'],
                        'instance': resource_info['database_id'].rsplit(':', 1)[-1]})


class SqlInstanceAction(MethodAction):

    def get_resource_params(self, model, resource):
        project, instance = self.path_param_re.match(
            resource['selfLink']).groups()
        return {'project': project, 'instance': instance}


@SqlInstance.action_registry.register('delete')
class SqlInstanceDelete(SqlInstanceAction):

    schema = type_schema('delete')
    method_spec = {'op': 'delete'}
    path_param_re = re.compile(
        '.*?/projects/(.*?)/instances/(.*)')


@SqlInstance.action_registry.register('stop')
class SqlInstanceStop(MethodAction):

    schema = type_schema('stop')
    method_spec = {'op': 'patch'}
    path_param_re = re.compile('.*?/projects/(.*?)/instances/(.*)')

    def get_resource_params(self, model, resource):
        project, instance = self.path_param_re.match(
            resource['selfLink']).groups()
        return {'project': project,
                'instance': instance,
                'body': {'settings': {'activationPolicy': 'NEVER'}}}


@SqlInstance.action_registry.register('set')
class SqlInstanceSet(SqlInstanceAction):
    """
    `Patches <https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/instances/patch>`_
    the 'Backup configuration' and 'Maintenance window' settings.

    The 'backup-configuration' setting requires at least one of 'start-time', 'enabled'
    or 'binary-log-enabled' parameters to be set. The 'hours' and 'minutes' settings
    for 'start-time' are passed to the API as a 'HH:MM'-formatted string. Note that
    GCP requires 'binary-log-enabled' to be disabled when 'enabled' is `False`,
    otherwise an exception represented by `binary_log_invalid_state_message` is raised.
    The `replicationLogArchivingEnabled` setting is "Reserved for future use" thus
    not implemented according to the `the resource documentation
    <https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/instances#resource>`_,

    The 'maintenance-window' setting configures the 'start-time' and 'update-track'
    options, at least one of which is expected to be provided. The 'day-of-week'
    parameter in 'start-time' requires a number from 1 (representing Monday) to 7 (Sunday)
    to be set while 'hour-of-day' is a value between 0 and 23 inclusive.
    The 'update-track' option accepts either 'canary' or 'stable' and is empty by default.

    .. code-block:: yaml

        policies:
          - name: gcp-sql-instance-set
            resource: gcp.sql-instance
            filters:
              - name: custodian-sql
            actions:
              - type: set
                backup-configuration:
                    start-time:
                        hours: 23
                        minutes: 59
                    enabled: true
                    binary-log-enabled: true
                maintenance-window:
                    restart-time:
                        day-of-week: 7
                        hour-of-day: 23
                    update-track: canary
    """
    schema = type_schema('set',
                         **{
                             'additionalProperties': False,
                             'backup-configuration': {
                                 'type': 'object',
                                 'additionalProperties': False,
                                 'minProperties': 1,
                                 'properties': {
                                     'start-time': {
                                         'type': 'object',
                                         'required': ['hours', 'minutes'],
                                         'additionalProperties': False,
                                         'properties': {
                                             'hours': {
                                                 'type': 'integer',
                                                 'minimum': 0,
                                                 'maximum': 23
                                             },
                                             'minutes': {
                                                 'type': 'integer',
                                                 'minimum': 0,
                                                 'maximum': 59
                                             }
                                         }
                                     },
                                     'enabled': {'type': 'boolean'},
                                     'binary-log-enabled': {'type': 'boolean'}
                                 }
                             },
                             'maintenance-window': {
                                 'type': 'object',
                                 'additionalProperties': False,
                                 'minProperties': 1,
                                 'properties': {
                                     'restart-time': {
                                         'type': 'object',
                                         'required': ['day-of-week', 'hour-of-day'],
                                         'additionalProperties': False,
                                         'properties': {
                                             'day-of-week': {
                                                 'type': 'integer',
                                                 'minimum': 1,
                                                 'maximum': 7
                                             },
                                             'hour-of-day': {
                                                 'type': 'integer',
                                                 'minimum': 0,
                                                 'maximum': 23
                                             }
                                         }
                                     },
                                     'update-track': {
                                         'type': 'string',
                                         'enum': ['canary', 'stable'],
                                     }
                                 }
                             }
                         })
    method_spec = {'op': 'patch'}
    path_param_re = re.compile('.*?/projects/(.*?)/instances/(.*)')
    binary_log_invalid_state_message = 'Binary log must be disabled when backup is disabled.'

    def get_resource_params(self, model, resource):
        project, instance = self.path_param_re.match(
            resource['selfLink']).groups()
        params = {'project': project,
                  'instance': instance,
                  'body': {'settings': {
                      'backupConfiguration': self._get_backup_configuration_params(resource),
                      'maintenanceWindow': self._get_maintenance_window_params(resource)
                  }}}
        return params

    def _get_backup_configuration_params(self, resource):
        params = {}
        data = self.data['backup-configuration'] if 'backup-configuration' in self.data else {}
        if 'start-time' in data:
            start_time = data['start-time']
            params['startTime'] = '%02d:%02d' % (start_time['hours'], start_time['minutes'])

        if 'enabled' in data:
            backup_enabled = data['enabled']
            params['enabled'] = backup_enabled
        else:
            backup_enabled = resource['settings']['backupConfiguration']['enabled']

        if 'binary-log-enabled' in data:
            binary_log_enabled = data['binary-log-enabled']
            if not backup_enabled and binary_log_enabled:
                raise ValueError(self.binary_log_invalid_state_message)
            params['binaryLogEnabled'] = binary_log_enabled
        return params

    def _get_maintenance_window_params(self, resource):
        params = {}
        data = self.data['maintenance-window'] if 'maintenance-window' in self.data else {}
        if 'restart-time' in data:
            params['day'] = data['restart-time']['day-of-week']
            params['hour'] = data['restart-time']['hour-of-day']
        if 'update-track' in data:
            params['updateTrack'] = data['update-track']
        return params


@resources.register('sql-user')
class SqlUser(ChildResourceManager):

    class resource_type(ChildTypeInfo):
        service = 'sqladmin'
        version = 'v1beta4'
        component = 'users'
        enum_spec = ('list', 'items[]', None)
        id = 'name'
        parent_spec = {
            'resource': 'sql-instance',
            'child_enum_params': [
                ('name', 'instance')
            ]
        }


class SqlInstanceChildWithSelfLink(ChildResourceManager):
    """A ChildResourceManager for resources that reference SqlInstance in selfLink.
    """

    def _get_parent_resource_info(self, child_instance):
        """
        :param child_instance: a dictionary to get parent parameters from
        :return: project_id and database_id extracted from child_instance
        """
        return {'project_id': re.match('.*?/projects/(.*?)/instances/.*',
                                    child_instance['selfLink']).group(1),
                'database_id': child_instance['instance']}


@resources.register('sql-backup-run')
class SqlBackupRun(SqlInstanceChildWithSelfLink):

    class resource_type(ChildTypeInfo):
        service = 'sqladmin'
        version = 'v1beta4'
        component = 'backupRuns'
        enum_spec = ('list', 'items[]', None)
        get_requires_event = True
        id = 'id'
        parent_spec = {
            'resource': 'sql-instance',
            'child_enum_params': [
                ('name', 'instance')
            ]
        }

        @staticmethod
        def get(client, event):
            project = jmespath.search('protoPayload.response.targetProject', event)
            instance = jmespath.search('protoPayload.response.targetId', event)
            insert_time = jmespath.search('protoPayload.response.insertTime', event)
            parameters = {'project': project,
                          'instance': instance,
                          'id': SqlBackupRun.resource_type._from_insert_time_to_id(insert_time)}
            return client.execute_command('get', parameters)

        @staticmethod
        def _from_insert_time_to_id(insert_time):
            """
            Backup Run id is not available in a log record directly.
            Fortunately, as it is an integer timestamp representation,
            it can be retrieved by converting raw insert_time value.

            :param insert_time: a UTC ISO formatted date time string
            :return: an integer number of microseconds since unix epoch
            """
            delta = parse(insert_time).replace(tzinfo=None) - datetime.utcfromtimestamp(0)
            return int(delta.total_seconds()) * 1000 + int(delta.microseconds / 1000)


@SqlBackupRun.action_registry.register('delete')
class SqlBackupRunDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/backupRuns/delete>`_
    the Backup taken by a Backup Run. The action does not specify any parameters.

    .. code-block:: yaml

        policies:
          - name: gcp-sql-backup-run-delete
            resource: gcp.sql-backup-run
            filters:
              - type: value
                value_type: age
                key: enqueuedTime
                value: 7
                op: ge
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        project, instance, backup_run_id = re.match(
            '.*/projects/(.+?)/instances/(.+?)/backupRuns/(.+)', r['selfLink']).groups()
        return {'project': project, 'instance': instance, 'id': backup_run_id}


@resources.register('sql-ssl-cert')
class SqlSslCert(SqlInstanceChildWithSelfLink):

    class resource_type(ChildTypeInfo):
        service = 'sqladmin'
        version = 'v1beta4'
        component = 'sslCerts'
        enum_spec = ('list', 'items[]', None)
        get_requires_event = True
        id = 'sha1Fingerprint'
        parent_spec = {
            'resource': 'sql-instance',
            'child_enum_params': [
                ('name', 'instance')
            ]
        }

        @staticmethod
        def get(client, event):
            self_link = jmespath.search('protoPayload.response.clientCert.certInfo.selfLink', event)
            self_link_re = '.*?/projects/(.*?)/instances/(.*?)/sslCerts/(.*)'
            project, instance, sha_1_fingerprint = re.match(self_link_re, self_link).groups()
            parameters = {'project': project,
                          'instance': instance,
                          'sha1Fingerprint': sha_1_fingerprint}
            return client.execute_command('get', parameters)
