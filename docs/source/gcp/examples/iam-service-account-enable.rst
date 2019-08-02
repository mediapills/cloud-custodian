IAM - Enable Service Account
============================

The example allows to enable filtered service accounts
which are contains similar displayName.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-enable
        resource: gcp.service-account
        filters:
          - type: value
            key: displayName
            op: contains
            value: {displayName}
        actions:
          - type: enable