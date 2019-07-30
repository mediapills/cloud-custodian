IAM - Update Project Roles name
==================================

The example allows to update filtered project roles name.

.. code-block:: yaml

    policies:
      - name: gcp-iam-project-role-update-title
        resource: gcp.project-role
        filters:
          - type: value
            key: title
            value: Custom Role
        actions:
          - type: set
            name: CustomRole1