Cloud Billing Accounts - Set IAM Policies
=========================================

The policy updates the IAM policy for Billing Accounts.

.. code-block:: yaml

    policies:
      - name: gcp-cloudbilling-account-set-iam-policy
        resource: gcp.cloudbilling-account
        filters:
          - type: value
            key: name
            value: billingAccounts/CU570D-1A4CU5-70D1A4
        actions:
          - type: set-iam-policy
            add-bindings:
              - members:
                  - user:user1@test.com
                  - user:user2@test.com
                role: roles/editor
            remove-bindings:
              - members: "*"
                role: roles/owner
