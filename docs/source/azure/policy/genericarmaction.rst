.. _azure_genericarmaction:

Generic Actions
================

These actions can be applied to a specific resource type, such as ``azure.vm``.

Tags
-----
``Tag``
  Add/Update tag on a resource

  .. c7n-schema:: azure.resourcegroup.actions.tag

  .. code-block:: yaml

        policies:
          - name: azure-tag
            resource: azure.resourcegroup
            description: |
              Tag all resource groups with 'mytag' with value 'myvalue'
            actions:
              - type: tag
                tag: mytag
                value: myvalue

``AutoTagUser``
  Create a tag listing name of user who created a resource based on scanning
  activity log history.

  .. c7n-schema:: azure.resourcegroup.actions.auto-tag-user

  .. code-block:: yaml

        policies:
          - name: azure-auto-tag-creator
            resource: azure.resourcegroup
            description: |
              Tag all existing resource groups with the 'CreatorEmail' tag
            actions:
              - type: auto-tag-user
                tag: CreatorEmail
                days: 10

``RemoveTag``
      Remove a set of tags.

      .. c7n-schema:: azure.vm.actions.untag

      .. code-block:: yaml

            policies:
              - name: tag-remove
                description: |
                  Removes tags from all virtual machines
                resource: azure.vm
                actions:
                 - type: untag
                   tags: ['TagName', 'TagName2']

``TagTrim``
    Automatically remove tags from an azure resource.

    Azure Resources and Resource Groups have a limit of 15 tags.
    In order to make additional tag space on a set of resources,
    this action can be used to remove enough tags to make the
    desired amount of space while preserving a given set of tags.
    Setting the space value to 0 removes all tags but those
    listed to preserve.

    .. c7n-schema:: azure.resourcegroup.actions.tag-trim

    .. code-block:: yaml

      - policies:
         - name: azure-tag-trim
           comment: |
             Any instances with 14 or more tags get tags removed until
             they match the target tag count, in this case 13, so
             that we free up tag slots for another usage.
           resource: azure.resourcegroup
           filters:
               # Filter down to resources that do not have the space
               # to add additional required tags. For example, if an
               # additional 2 tags need to be added to a resource, with
               # 15 tags as the limit, then filter down to resources that
               # have 14 or more tags since they will need to have tags
               # removed for the 2 extra. This also ensures that metrics
               # reporting is correct for the policy.
               type: value
               key: "[length(Tags)][0]"
               op: ge
               value: 14
           actions:
             - type: tag-trim
               space: 2
               preserve:
                - OwnerContact
                - Environment
                - downtime
                - custodian_status

Delayed operations
------------------

``mark-for-op``
    Mark Azure resources for a future operations via tags.

    .. c7n-schema:: azure.vm.actions.mark-for-op

Examples
~~~~~~~~

- :ref:`azure_example_delayedoperation`

Logic App
---------

``LogicApp``
  Call the HTTP Endpoint on an Azure Logic App.

  Your policy credentials are used to get the trigger endpoint URL with secrets
  using the resource group and app name.

  This action is based on the ``webhook`` action and supports the same options.

  .. c7n-schema:: azure.vm.actions.logic-app

  .. code-block:: yaml

      policies:
        - name: call-logic-app
          resource: azure.vm
          description: |
            Call logic app with list of VM's
          actions:
           - type: logic-app
             resource-group: custodian-test
             logic-app-name: cclogicapp
             batch: true
             body: 'resources[].{ vm_name: name }'

Delete
-------

``DeleteAction``
      Perform delete operation on any ARM resource. Can be used with 
      generic resource type `armresource` or on any other more specific
      ARM resource type supported by Cloud Custodian.

      .. c7n-schema:: azure.networksecuritygroup.actions.delete

      .. code-block:: yaml

          - policies:
              - name: delete-test-resources
                description: |
                  Deletes any ARM resource with 'test' in the name
                resource: azure.armresource
                filters:
                 - type: value
                   name: test
                   op: in
                actions:
                 - type: delete

      The delete action also works with a specified resource type:

      .. code-block:: yaml

          - policies:
              - name: delete-test-nsg
                description: |
                  Deletes any Network Security Group with 'test' in the name
                resource: azure.networksecuritygroup
                filters:
                 - type: value
                   name: test
                   op: in
                actions:
                 - type: delete
