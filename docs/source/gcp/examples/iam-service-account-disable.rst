IAM - Disable Service Account
=============================

The example allows to disable filtered service accounts
which are contains similar displayName.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-disable
        resource: gcp.service-account
        filters:
          - type: value
            key: displayName
            value: {displayName}
        actions:
          - type: disable