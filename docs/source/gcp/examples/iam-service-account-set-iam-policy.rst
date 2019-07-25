IAM - Enforce IAM policies of Service Accounts
=============================================

Custodian can control IAM policies of target resources and enforce an approved hard-coded configuration removing all custom changes in permissions (if any).

The policy below updates IAM policy for spanner instances and databases.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml
    policies:
    - name: gcp-spanner-instances-set-iam-policy
      resource: gcp.spanner-instance
      actions:
      - type: set-iam-policy
        bindings:
        - members:
          - user:user1@test.com
          - user2@test.com
          role: roles/owner
        - members:
          - user:user3@gmail.com
          role: roles/viewer
    - name: gcp-spanner-database-instances-set-iam-policy
      resource: gcp.spanner-database-instance
      actions:
      - type: set-iam-policy
        bindings:
        - members:
          - user:user1@test.com
          - user2@test.com
          role: roles/owner
        - members:
          - user:user3@gmail.com
          role: roles/viewer
