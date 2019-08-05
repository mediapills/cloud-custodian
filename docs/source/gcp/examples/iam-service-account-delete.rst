IAM - Delete Service Account
============================

The example allows to delete filtered service accounts
which contain similar displayName.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-delete
        resource: gcp.service-account
        filters:
          - type: value
            key: displayName
            op: contains
            value: {displayName}
        actions:
          - type: delete