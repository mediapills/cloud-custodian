IAM - Delete Project Roles
==========================

To enforce security of your projects, Custodian can automatically delete any role which match its filter.

The policy below deletes all roles with deprecated or beta status.

.. code-block:: yaml

    policies:
      - name: gcp-iam-project-role
        resource: gcp.project-role
        filters:
          - type: value
            key: email
            op: regex
            value: ^projects\/.+\/roles\/.+$
        actions:
          - type: delete
