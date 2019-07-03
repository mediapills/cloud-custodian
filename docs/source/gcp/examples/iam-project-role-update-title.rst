IAM - Update filtered project role title
========================================

The example allows to update filtered project role title.

.. code-block:: yaml

    policies:
      - name: gcp-iam-project-role-update-title
        resource: gcp.project-role
        filters:
          - type: value
            key: title
            value: Custom Role
        actions:
          - type: update-title
            name: CustomRole1