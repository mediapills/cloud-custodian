Billing Accounts - Set IAM Policies
===================================

Custodian can ensure that your billing accounts have an approved and controlled set of permissions.

This sample policy updates the IAM policy for the specified billing account.

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
