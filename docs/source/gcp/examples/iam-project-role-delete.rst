IAM - Delete filtered project role
==================================

The example allows to delete filtered project role.

.. code-block:: yaml

     policies:
      - name: gcp-iam-project-role
        resource: gcp.project-role
        filters:
          - type: value
            key: title
            value: Custom Role
        actions:
          - type: delete