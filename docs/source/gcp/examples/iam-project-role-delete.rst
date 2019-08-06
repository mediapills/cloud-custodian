IAM - Delete Project Roles
==========================

To enforce security of your organization, Custodian can automatically delete any role which match its filter.

The policy below deletes all roles with deprecated or beta status.

.. code-block:: yaml

    policies:
      - name: gcp-iam-project-role
        resource: gcp.project-role
        filters:
          - type: value
            key: stage
            op: in
            value: [BETA, DEPRECATED]
        actions:
          - type: delete
