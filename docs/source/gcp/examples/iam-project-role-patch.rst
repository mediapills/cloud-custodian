IAM - Update Project Roles includedPermissions
==============================================

The example allows to set includedPermissions for project roles
which contain similar title.

.. code-block:: yaml

    policies:
      - name: gcp-iam-project-role-set-permissions
        resource: gcp.project-role
        filters:
          - type: value
            key: title
            op: contains
            value: Custom Role
        actions:
          - type: set
            includedPermissions:
              - appengine.services.delete
              - accessapproval.requests.approve
