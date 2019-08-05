IAM - Update filtered service account description
==================================================

The example allows to update service accounts description
which contain similar displayName.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-set-display-name
        resource: gcp.service-account
        filters:
          - type: value
            key: displayName
            op: contains
            value: {displayName}
        actions:
          - type: set
            description: test-name