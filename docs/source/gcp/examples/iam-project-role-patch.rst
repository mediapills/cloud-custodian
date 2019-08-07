IAM - Update Project Roles Permissions
======================================

The policy below updates a set of permissions for all project roles that contain a specified word in title.

.. code-block:: yaml

    policies:
      - name: gcp-iam-project-role-set-permissions
        resource: gcp.project-role
        filters:
          - type: value
            key: title
            op: contains
            value: executor
        actions:
          - type: set
            includedPermissions:
              - appengine.services.delete
              - accessapproval.requests.approve
