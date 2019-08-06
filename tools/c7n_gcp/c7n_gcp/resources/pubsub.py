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

from c7n.utils import type_schema

from c7n_gcp.actions import MethodAction
from c7n_gcp.provider import resources
from c7n_gcp.query import QueryResourceManager, TypeInfo
from datetime import timedelta

"""
todo, needs detail_spec
"""


@resources.register('pubsub-topic')
class PubSubTopic(QueryResourceManager):
    """GCP resource: https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics
    """
    class resource_type(TypeInfo):
        service = 'pubsub'
        version = 'v1'
        component = 'projects.topics'
        enum_spec = ('list', 'topics[]', None)
        scope_template = "projects/{}"
        id = "name"

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'topic': resource_info['topic_id']})


@PubSubTopic.action_registry.register('delete')
class PubSubTopicDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/delete>`_
    a Pub/Sub Topic. The action does not specify any parameters.

    .. code-block:: yaml

        policies:
          - name: gcp-pubsub-topic-delete
            resource: gcp.pubsub-topic
            filters:
              - type: value
                key: name
                value: projects/cloud-custodian/topics/topic-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        return {'topic': r['name']}


@resources.register('pubsub-subscription')
class PubSubSubscription(QueryResourceManager):
    """GCP resource: https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions
    """
    class resource_type(TypeInfo):
        service = 'pubsub'
        version = 'v1'
        component = 'projects.subscriptions'
        enum_spec = ('list', 'subscriptions[]', None)
        scope_template = 'projects/{}'
        id = 'name'

        @staticmethod
        def get(client, resource_info):
            return client.execute_command(
                'get', {'subscription': resource_info['subscription_id']})


@PubSubSubscription.action_registry.register('delete')
class PubSubSubscriptionDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/delete>
    `_ a Pub/Sub Subscription. The action does not specify any parameters.

    .. code-block:: yaml

        policies:
          - name: gcp-pubsub-subscription-delete
            resource: gcp.pubsub-subscription
            filters:
              - type: value
                key: name
                value: projects/cloud-custodian/subscriptions/subscription-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        return {'subscription': r['name']}


@PubSubSubscription.action_registry.register('set')
class PubSubSubscriptionSet(MethodAction):
    """
    `Patches <https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/patch>`_
    the 'Subscription expiration' and 'Message retention duration' settings.

    The 'expiration-policy-ttl' setting requires the 'days' parameter to either be 0
    meaning unsetting the policy or a positive integer up to 365 that will be further
    converted into 'expirationPolicy.ttl' seconds.

    The 'message-retention-duration' requires at least one of 'days', 'hours' or 'minutes'
    parameters to be set from 10 minutes to 7 days in total that will be further converted
    into 'messageRetentionDuration' seconds.

    Note that the 'Message retention duration' value cannot be greater than the 'Subscription
    expiration' value (unless 'Message retention duration' is 0), otherwise an exception
    represented by 'retention_duration_cannot_exceed_ttl_message' is raised (which mirrors the API).

    .. code-block:: yaml

        policies:
          - name: gcp-pubsub-subscription-set
            resource: gcp.pubsub-subscription
            filters:
              - type: value
                key: name
                value: projects/cloud-custodian/subscriptions/subscription-to-update
            actions:
              - type: set
                expiration-policy-ttl:
                  days: 2
                message-retention-duration:
                  days: 1
                  hours: 2
                  minutes: 3
    """
    schema = type_schema('set',
                         **{
                             'expiration-policy-ttl': {
                                 'type': 'object',
                                 'required': ['days'],
                                 'additionalProperties': False,
                                 'properties': {
                                     'days': {
                                         'type': 'integer',
                                         'minimum': 0,
                                         'maximum': 365
                                     }
                                 }
                             },
                             'message-retention-duration': {
                                 'type': 'object',
                                 'additionalProperties': False,
                                 'minProperties': 1,
                                 'properties': {
                                     'days': {
                                         'type': 'integer',
                                         'minimum': 0,
                                         'maximum': 7
                                     },
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
                             }
                         })
    method_spec = {'op': 'patch'}
    retention_duration_cannot_exceed_ttl_message = 'The subscription\'s message retention ' \
                                                   'duration (%ss) cannot be greater than ' \
                                                   'the TTL in the subscription\'s expiration ' \
                                                   'policy (%ss), since messages cannot ' \
                                                   'be retained past subscription expiration.'
    retention_duration_out_of_bounds_message = 'The value for message retention duration is ' \
                                               'out of bounds. You passed %ss in the request, ' \
                                               'but the value must be between 10m and 168h.'

    def get_resource_params(self, m, r):
        expiration_seconds = self._get_expiration_policy_ttl_seconds(r)
        retention_seconds = self._get_message_retention_duration_seconds(r)
        if retention_seconds > expiration_seconds:
            raise ValueError(self.retention_duration_cannot_exceed_ttl_message
                             % (retention_seconds, expiration_seconds))
        params = {'name': r['name'],
                  'body': {
                      'subscription': {
                          'expirationPolicy': {},
                          'messageRetentionDuration': "%ds" % retention_seconds
                      },
                      'updateMask': 'expiration_policy,message_retention_duration'}}
        if expiration_seconds > 0:
            params['body']['subscription']['expirationPolicy']['ttl'] = "%ds" % expiration_seconds
        return params

    def _get_expiration_policy_ttl_seconds(self, r):
        """
        Returns an integer number of seconds for the 'Subscription expiration' setting.

        :param r: the same as in :func:`get_resource_params`
        :return: the days converted to seconds if set in self.data['expiration-policy-ttl']
                 or the existing value extracted from r['expirationPolicy'] otherwise
        """
        if 'expiration-policy-ttl' in self.data:
            days = self.data['expiration-policy-ttl']['days']
            return int(timedelta(days=days).total_seconds()) if days > 0 else 0
        else:
            expiration_policy = r['expirationPolicy']
            return int(re.match('(.+)s', expiration_policy['ttl'])
                       .group(1)) if 'ttl' in expiration_policy else 0

    def _get_message_retention_duration_seconds(self, r):
        """
        Returns an integer number of seconds for the 'Message retention duration' setting.

        :param r: the same as in :func:`get_resource_params`
        :return: the days, hours and minutes converted to seconds if set
                 in self.data['message-retention-duration']
                 or the existing value extracted from r['messageRetentionDuration'] otherwise
        """
        if 'message-retention-duration' in self.data:
            duration = self.data['message-retention-duration']
            days = duration['days'] if 'days' in duration else 0
            hours = duration['hours'] if 'hours' in duration else 0
            minutes = duration['minutes'] if 'minutes' in duration else 0
            duration_seconds = int(timedelta(days=days, hours=hours, minutes=minutes)
                                   .total_seconds())
            min_duration_seconds = int(timedelta(minutes=10).total_seconds())
            max_duration_seconds = int(timedelta(hours=168).total_seconds())
            if duration_seconds < min_duration_seconds or max_duration_seconds < duration_seconds:
                raise ValueError(self.retention_duration_out_of_bounds_message % duration_seconds)
            return duration_seconds
        else:
            return int(re.match('(.+)s', r['messageRetentionDuration']).group(1))


@resources.register('pubsub-snapshot')
class PubSubSnapshot(QueryResourceManager):
    """GCP resource: https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.snapshots
    """
    class resource_type(TypeInfo):
        service = 'pubsub'
        version = 'v1'
        component = 'projects.snapshots'
        enum_spec = ('list', 'snapshots[]', None)
        scope_template = 'projects/{}'
        id = 'name'


@PubSubSnapshot.action_registry.register('delete')
class PubSubSnapshotDelete(MethodAction):
    """
    `Deletes <https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.snapshots/delete>`_
    a Pub/Sub Snapshot. The action does not specify any parameters.

    .. code-block:: yaml

        policies:
          - name: gcp-pubsub-snapshot-delete
            resource: gcp.pubsub-snapshot
            filters:
              - type: value
                key: name
                value: projects/cloud-custodian/snapshots/snapshot-to-delete
            actions:
              - type: delete
    """
    schema = type_schema('delete')
    method_spec = {'op': 'delete'}

    def get_resource_params(self, m, r):
        return {'snapshot': r['name']}
