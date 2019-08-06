IAM - Disable Service Account
=============================

It's a best security practice to avoid usage of real purpose of service accounts in their names. 

This policy disables all service accounts that contains blacklisted words.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-disable
        resource: gcp.service-account
        filters:
          - type: value
            key: displayName
            op: in
            value: [accounting, privacy, confidential]
        actions:
          - type: disable
