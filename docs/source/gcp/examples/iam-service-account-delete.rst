IAM - Delete Service Accounts
=============================

It's always a good idea to control conventions across service accounts in your organization.

This sample policy deletes all service accounts where email do not match an established pattern.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-delete
        resource: gcp.service-account
        filters:
          - type: value
            key: email
            op: regex
            value: ^special[a-zA-Z0-9_]+@cloudcustodian\.io$
        actions:
          - type: delete
