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

import jmespath
from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo, ChildResourceManager, ChildTypeInfo,\
    GcpLocation

from c7n.utils import local_session, type_schema


@resources.register('cloudtasks-queue')
class CloudTasksQueue(QueryResourceManager):
    """GCP resource:
    https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues
    """
    class resource_type(TypeInfo):
        service = 'cloudtasks'
        version = 'v2'
        component = 'projects.locations.queues'
        enum_spec = ('list', 'queues[]', None)
        scope = None
        get_requires_event = True
        id = 'name'

        @staticmethod
        def get(client, event):
            return client.execute_query(
                'get', {'name': jmespath.search('protoPayload.response.name', event)})

    def get_resource_query(self):
        if 'query' in self.data:
            for child in self.data.get('query'):
                if 'location' in child:
                    location_query = child['location']
                    return {'parent': location_query if isinstance(
                        location_query, list) else [location_query]}

    def _fetch_resources(self, query):
        session = local_session(self.session_factory)
        project = session.get_default_project()
        locations = query['parent'] if query and 'parent' in query else GcpLocation.app_locations
        project_locations = ['projects/{}/locations/{}'.format(project, location)
                             for location in locations]
        key_rings = []
        for location in project_locations:
            key_rings.extend(QueryResourceManager._fetch_resources(self, {'parent': location}))
        return key_rings


@CloudTasksQueue.action_registry.register('delete')
class CloudTaskQueueDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues
    /delete>`_ a Task Queue. The action does not specify any parameters.

    Example:
    .. code-block:: yaml

        policies:
          - name: gcp-cloudtasks-queue-set
            resource: gcp.cloudtasks-queue
            filters:
              - type: value
                key: name
                value: projects/target-project/locations/target-location/queues/queue-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        return {'name': r['name']}


@CloudTasksQueue.action_registry.register('set')
class CloudTaskQueueSet(MethodAction):
    """
    `Patches <https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues
    /patch>`_ a Task Queue.

    The 'rate-limits' block determines the maximum rate that tasks can be dispatched by a queue,
    regardless of whether the dispatch is a first task attempt or a retry. It consists of the
    'max-concurrent-dispatches' and 'max-dispatches-per-second' integer parameters that can be set
    either separately or together and whose maximal values are defined in the schema according to
    the API documentation. Note that the following behavior takes place when 0 is passed:
     - 'max-concurrent-dispatches' integer parameter resets to 1000;
     - 'max-dispatches-per-second' integer parameter resets to its max value 500.

    The 'retry-config' block determines when a failed task attempt is retried. All the parameters
    allowed there - 'max-attempts', 'max-backoff', 'max-doublings', 'max-retry-duration', and
    'min-backoff' - have been made integers in Custodian though 'max-backoff', 'max-retry-duration',
    and 'min-backoff' are floating-point seconds formatted as '%fs' in the API according to the
    `documentation <https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues
    #RetryConfig>`_ of which the values are truncated to the nearest second thus the fractional part
    does not actually make any difference. Note the following behavior when 0 is passed:
     - 'max-attempts' resets to 100;
     - 'max-backoff' resets to 3600s;
     - 'max-doublings' resets to 16;
     - 'max-retry-duration' becomes a hidden field and is treated as 'ulimited';
     - 'min-backoff' resets to 0.100s.
    The 'max-attempts' parameter also supports the special -1 value indicating unlimited attempts.
    The 'min_backoff_greater_than_max_backoff_error' `ValueError` is raised when 'min-backoff'
    is not less than or equal to 'max-backoff' which mirrors the API behavior.

    All the parameters mentioned above are set using the `_set_best_available_value` method
    in order to prevent the existing values to be overwritten by the default ones.

    Example:
    .. code-block:: yaml

        policies:
          - name: gcp-cloudtasks-queue-set
            resource: gcp.cloudtasks-queue
            filters:
              - type: value
                key: name
                value: projects/target-project/locations/target-location/queues/queue-to-set
            actions:
              - type: set
                rate-limits:
                    max-concurrent-dispatches: 2
                    max-dispatches-per-second: 3
                retry-config:
                    max-attempts: 4
                    max-backoff: 8
                    max-doublings: 6
                    max-retry-duration: 7
                    min-backoff: 5
    """
    schema = type_schema('set',
                         **{
                             'additionalProperties': False,
                             'rate-limits': {
                                 'additionalProperties': False,
                                 'minProperties': 1,
                                 'properties': {
                                     'max-concurrent-dispatches': {
                                         'type': 'integer',
                                         'minimum': 0,
                                         'maximum': 5000
                                     },
                                     'max-dispatches-per-second': {
                                         'type': 'integer',
                                         'minimum': 0,
                                         'maximum': 500
                                     }
                                 }
                             },
                             'retry-config': {
                                 'additionalProperties': False,
                                 'minProperties': 1,
                                 'properties': {
                                     'max-attempts': {
                                         'type': 'integer',
                                         'minimum': -1
                                     },
                                     'max-backoff': {
                                         'type': 'integer',
                                         'minimum': 0
                                     },
                                     'max-doublings': {
                                         'type': 'integer',
                                         'minimum': 0
                                     },
                                     'max-retry-duration': {
                                         'type': 'integer',
                                         'minimum': 0
                                     },
                                     'min-backoff': {
                                         'type': 'integer',
                                         'minimum': 0
                                     }
                                 }
                             }
                         })
    method_spec = {'op': 'patch'}
    min_backoff_greater_than_max_backoff_error = ('RetryConfig.minBackoff (%s) must be less than '
                                                  'or equal to RetryConfig.maxBackoff (%s)')
    not_seconds_formatted_string_error = 'A \'%%fs\'-formatted string expected (actual - \'%s\')'

    def get_resource_params(self, m, r):
        """
        :param r: the resource dict the action applies to
        :raises ValueError: if raised by `_get_retry_config`
        """
        params = {'name': r['name'], 'body': {}}
        rate_limits = self._get_rate_limits(r)
        if rate_limits:
            params['body']['rateLimits'] = rate_limits
        retry_config = self._get_retry_config(r)
        if retry_config:
            params['body']['retryConfig'] = retry_config
        return params

    def _get_rate_limits(self, r):
        """
        If successful, returns a dict with the 'maxConcurrentDispatches' and
        'maxDispatchesPerSecond' parameters set with `_set_best_available_value`.

        :param r: the same as in get_resource_params
        :return: either `None` or a dict to place into params['body']['rateLimits']
        """
        if 'rate-limits' not in self.data:
            return None

        rate_limits = {}
        rl_data = self.data['rate-limits']
        rl_subdict = r['rateLimits'] if 'rateLimits' in r else {}
        self._set_best_available_value(
            rate_limits, rl_data, rl_subdict,
            'max-concurrent-dispatches', 'maxConcurrentDispatches')
        self._set_best_available_value(
            rate_limits, rl_data, rl_subdict, 'max-dispatches-per-second', 'maxDispatchesPerSecond')
        return rate_limits

    def _get_retry_config(self, r):
        """
        If successful, returns a dict with the 'maxAttempts', 'maxBackoff', 'maxDoublings',
        'maxRetryDuration', and 'minBackoff' parameters set with `_set_best_available_value`.

        :param r: the same as in get_resource_params
        :return: either `None` or a dict to place into params['body']['retryConfig']
        :raises ValueError: if 'min-backoff' is greater than 'max-backoff' or if `_extract_seconds`
                            decides to
        """
        if 'retry-config' not in self.data:
            return None

        retry_config = {}
        rc_data = self.data['retry-config']
        rc_subdict = r['retryConfig'] if 'retryConfig' in r else {}
        self._set_best_available_value(
            retry_config, rc_data, rc_subdict, 'max-attempts', 'maxAttempts')
        self._set_best_available_value(
            retry_config, rc_data, rc_subdict, 'max-backoff', 'maxBackoff', True)
        self._set_best_available_value(
            retry_config, rc_data, rc_subdict, 'max-doublings', 'maxDoublings')
        self._set_best_available_value(
            retry_config, rc_data, rc_subdict, 'max-retry-duration', 'maxRetryDuration', True)
        self._set_best_available_value(
            retry_config, rc_data, rc_subdict, 'min-backoff', 'minBackoff', True)
        if 'minBackoff' in retry_config and 'maxBackoff' in retry_config:
            min_b_string = retry_config['minBackoff']
            max_b_string = retry_config['maxBackoff']
            if self._extract_seconds(min_b_string) > self._extract_seconds(max_b_string):
                raise ValueError(self.min_backoff_greater_than_max_backoff_error
                                 % (min_b_string, max_b_string))
        return retry_config

    def _set_best_available_value(self, destination_params, data_dict, r_subdict,
                                  data_key, r_key, format_as_seconds=False):
        """
        Tries to:
         1) get a value at `data_key` from `data_dict;
         2) format the value if successfully got in step 1 and `format_as_seconds` is `True`;
         3) get a value at `r_key` from `r_subdict` unless step 1 has been successful;
         4) set the value at `r_key` to `destination_params` if either step 1 or 3 has succeeded.

        '%ds' is meant by a seconds-formatted string. As an integer (%d) is expected, the method is
        not designed to work with other types which is perfectly fine in the scope of the current
        Action though could be changed with a little effort required if needed.

        :param destination_params: a dict to write the value to
        :param data_dict: a dict to try first to get the value from by `data_key`, and convert to
                          a seconds-formatted string if `format_as_seconds` is `True`
        :param r_subdict: a dict to try second to get the value from by `r_key`
        :param data_key: a string key to get value at from `data_dict`
        :param r_key: a string key to get value at from `r_subdict` and write data at
                      to `destination_params`
        :param format_as_seconds: (optional, `False` by default) a boolean flag indicating whether
                                  the value at `data_key` from `data_dict` should be converted to
                                  a seconds-formatted string
        """
        data_dict_value = data_dict[data_key] if data_key in data_dict else None
        data_dict_value_not_none = data_dict_value is not None
        if data_dict_value_not_none and format_as_seconds:
            data_dict_value = '%ds' % data_dict_value
        value = (data_dict_value if data_dict_value_not_none
                 else r_subdict[r_key] if r_key in r_subdict else None)
        if value is not None:
            destination_params[r_key] = value

    def _extract_seconds(self, seconds_formatted_string):
        """
        If a string is a floating-point number concatenated with 's', returns a `float`
        representation of the number. Otherwise, raises a `not_seconds_formatted_string_error`.

        :param seconds_formatted_string: a string to parse
        :raises ValueError: unless the provided string is properly formatted
        """
        match = re.match('(.+)s', seconds_formatted_string)
        if match is None:
            raise ValueError(self.not_seconds_formatted_string_error % seconds_formatted_string)
        return float(match.group(1))


@resources.register('cloudtasks-task')
class CloudTask(ChildResourceManager):
    """GCP resource:
    https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues.tasks
    """
    def _get_child_enum_args(self, parent_instance):
        return {'parent': parent_instance['name']}

    def _get_parent_resource_info(self, child_instance):
        return {'protoPayload': {'response': {
            'name': re.match('(projects/.*?/locations/.*?/queues/.*?)/tasks/.*',
                             child_instance['name']).group(1)}}}

    class resource_type(ChildTypeInfo):
        service = 'cloudtasks'
        version = 'v2'
        component = 'projects.locations.queues.tasks'
        enum_spec = ('list', 'tasks[]', None)
        scope = None
        id = 'name'
        parent_spec = {
            'resource': 'cloudtasks-queue'
        }

        @staticmethod
        def get(client, resource_info):
            return client.execute_query(
                'get', {'name': resource_info['resourceName']})


@CloudTask.action_registry.register('delete')
class CloudTaskDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations.queues.tasks
    /delete>`_ a Task. The action does not specify any parameters.

    Example:
    .. code-block:: yaml

        policies:
          - name: gcp-cloudtasks-task-delete
            resource: gcp.cloudtasks-task
            filters:
              - type: value
                key: name
                value: "projects/target-project/locations/target-location/queues/target-queue/tasks\
                       /task-to-delete"
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        return {'name': r['name']}
