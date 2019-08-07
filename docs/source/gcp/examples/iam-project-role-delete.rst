IAM - Delete Project Roles
==========================

To enforce security of your projects, Custodian can automatically delete any role that matches its filter.

The policy below deletes all roles containing 'logging.viewer' in their names.

.. code-block:: yaml

    policies:
      - name: gcp-iam-project-role
        resource: gcp.project-role
        filters:
          - type: value
            key: name
            op: regex
            value: ^[a-zA-Z0-9\/]+\/logging.viewer$
        actions:
          - type: delete
