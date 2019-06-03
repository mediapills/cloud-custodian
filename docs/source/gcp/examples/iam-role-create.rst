IAM - Notify users about new roles creation
============================================================

The following example policies will allow you to notify your Admin about new roles creation. Also you can extend this policy and add permission filtering to control access.

.. code-block:: yaml

    policies:
      - name: iam-role-policy
        description: |
          Notify IAM role created
        resource: gcp.project-role
        mode:
          type: gcp-audit
          methods:
          - "google.iam.admin.v1.CreateRole"
        actions:
          - type: notify
            subject: IAM role has been created
            to:
              - Pub/Sub
            transport:
              type: pubsub
              topic: projects/mythic-tribute-232915/topics/iam-demo
