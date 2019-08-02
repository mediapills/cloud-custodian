IAM - Delete Project Roles
==========================

To enforce security of your organization, Custodian can automatically delete any
role which contains similar title.

.. code-block:: yaml

     policies:
      - name: gcp-iam-project-role
        resource: gcp.project-role
        filters:
          - type: value
            key: title
            op: contains
            value: Custom Role
        actions:
          - type: delete
