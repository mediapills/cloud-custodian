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

from c7n.utils import local_session, type_schema
from c7n_gcp.actions import MethodAction


class SetIamPolicy(MethodAction):
    """ Sets IAM policy. It works with bindings only.

        The action executes in one of the two modes defined by a policy:
        - add,
        - remove.

        The `add` mode merges the existing bindings with the ones in the policy, hereby no changes
        are made if all the required bindings are already present in the applicable resource. The
        `remove` mode filters out the existing bindings against the provided ones, so the action
        will take no effect if there are no matches. For more information, please refer to the
        `_add_bindings` and `_remove_bindings` methods respectively.

        There following member types are available to work with:
        - allUsers,
        - allAuthenticatedUsers,
        - user,
        - group,
        - domain,
        - serviceAccount.

        Note the `resource` field in the example that could be changed to another resource that has
        both `setIamPolicy` and `getIamPolicy` methods (such as gcp.spanner-database-instance).

        Example:

        .. code-block:: yaml

            policies:
              - name: gcp-spanner-instance-set-iam-policy
                resource: gcp.spanner-instance
                actions:
                  - type: set-iam-policy
                    mode: add
                    bindings:
                      - members:
                          - user:user1@test.com
                          - user:user2@test.com
                        role: roles/owner
                      - members:
                          - user:user3@gmail.com
                        role: roles/viewer
        """
    schema = type_schema('set-iam-policy',
                         required=['bindings', 'mode'],
                         **{
                             'bindings': {
                                 'type': 'array',
                                 'minItems': 1,
                                 'items': {'role': {'type': 'string'},
                                           'members': {'type': 'array',
                                                       'items': {
                                                           'type': 'string'},
                                                       'minItems': 1}}
                             },
                             'mode': {'type': 'string', 'enum': ['add', 'remove']}
                         })
    method_spec = {'op': 'setIamPolicy'}
    schema_alias = True

    def get_resource_params(self, model, resource):
        """
        Depending on the `mode` specified in a policy, calls either `_add_bindings` or
        `_remove_bindings`, then sets the resulting list at the 'bindings' key if there is at least
        a single record there, or assigns an empty object to the 'policy' key in order to
        avoid errors produced by the API.

        :param model: the parameters that are defined in a resource manager
        :param resource: the resource the action is applied to
        """
        existing_bindings = self._get_existing_bindings(model, resource)
        new_bindings = self.data['bindings']
        bindings_to_set = (self._add_bindings(existing_bindings, new_bindings)
                           if self.data['mode'] == 'add'
                           else self._remove_bindings(existing_bindings, new_bindings))
        return {'resource': resource['name'], 'body': {
            'policy': {'bindings': bindings_to_set} if len(bindings_to_set) > 0 else {}}}

    def _get_existing_bindings(self, model, resource):
        """
        Calls the `getIamPolicy` method on the resource the action is applied to and returns
        either a list of existing bindings or an empty one if there is no 'bindings' key.

        :param model: the same as in `get_resource_params` (needed to take `component` from)
        :param resource: the same as in `get_resource_params` (passed into `_verb_arguments`)
        """
        existing_bindings = local_session(self.manager.session_factory).client(
            self.manager.resource_type.service,
            self.manager.resource_type.version,
            model.component).execute_query(
            'getIamPolicy', verb_arguments=self._verb_arguments(resource))
        return existing_bindings['bindings'] if 'bindings' in existing_bindings else []

    def _verb_arguments(self, resource):
        """
        Returns a dictionary that is passed when making the `getIamPolicy` API call.

        :param resource: the same as in `get_resource_params`
        """
        return {'resource': resource['name']}

    def _add_bindings(self, existing_bindings, bindings_to_add):
        """
        Converts the provided lists using `_get_roles_to_bindings_dict`, then iterates through
        them so that the returned list combines:
        - among the roles mentioned in a policy, the existing members merged with the ones to add
          so that there are no duplicates,
        - as for the other roles, all their members.

        The roles or members that are mentioned in the policy and already present
        in the existing bindings are simply ignored with no errors produced.

        An empty list could be returned only if both `existing_bindings` and `bindings_to_remove`
        are empty, the possibility of which is defined by the caller of the method.

        For additional information on how the method works, please refer to the tests
        (e.g. test_spanner).

        :param existing_bindings: a list of dictionaries containing the 'role' and 'members' keys
                                  taken from the resource the action is applied to
        :param bindings_to_add: a list of dictionaries containing the 'role' and 'members' keys
                                taken from the policy
        """
        bindings = []
        roles_to_existing_bindings = self._get_roles_to_bindings_dict(existing_bindings)
        roles_to_bindings_to_add = self._get_roles_to_bindings_dict(bindings_to_add)
        for role in roles_to_bindings_to_add:
            updated_members = dict(roles_to_bindings_to_add[role])
            if role in roles_to_existing_bindings:
                existing_members = roles_to_existing_bindings[role]['members']
                members_to_add = list(filter(lambda member: member not in existing_members,
                                             updated_members['members']))
                updated_members['members'] = existing_members + members_to_add
            bindings.append(updated_members)

        for role in roles_to_existing_bindings:
            if role not in roles_to_bindings_to_add:
                bindings.append(roles_to_existing_bindings[role])
        return bindings

    def _remove_bindings(self, existing_bindings, bindings_to_remove):
        """
        Converts the provided lists using `_get_roles_to_bindings_dict`, then iterates through
        them so that the returned list combines:
        - among the roles mentioned in a policy, only the members that are not marked for removal,
        - as for the other roles, all their members.

        The roles or members that are mentioned in the policy but are absent
        in the existing bindings are simply ignored with no errors produced.

        As can be observed, it is possible to have an empty list returned either if
        `existing_bindings` is already empty or `bindings_to_remove` filters everything out.

        For additional information on how the method works, please refer to the tests
        (e.g. test_spanner).

        :param existing_bindings: a list of dictionaries containing the 'role' and 'members' keys
                                  taken from the resource the action is applied to
        :param bindings_to_remove: a list of dictionaries containing the 'role' and 'members' keys
                                   taken from the policy
        """
        bindings = []
        roles_to_existing_bindings = self._get_roles_to_bindings_dict(existing_bindings)
        roles_to_bindings_to_remove = self._get_roles_to_bindings_dict(bindings_to_remove)
        for role in roles_to_bindings_to_remove:
            if role in roles_to_existing_bindings:
                updated_members = dict(roles_to_existing_bindings[role])
                members_to_remove = roles_to_bindings_to_remove[role]
                updated_members['members'] = list(filter(
                    lambda member: member not in members_to_remove['members'],
                    updated_members['members']))
                if len(updated_members['members']) > 0:
                    bindings.append(updated_members)

        for role in roles_to_existing_bindings:
            if role not in roles_to_bindings_to_remove:
                bindings.append(roles_to_existing_bindings[role])
        return bindings

    def _get_roles_to_bindings_dict(self, bindings_list):
        """
        Converts a given list to a dictionary, values under the 'role' key in elements of whose
        become keys in the resulting dictionary while the elements themselves become values
        associated with these keys.

        :param bindings_list: a list whose elements are expected to have the 'role' key
        """
        return {binding['role']: binding for binding in bindings_list}
