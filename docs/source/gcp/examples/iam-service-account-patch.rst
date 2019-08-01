IAM - Update filtered service account display name
==================================================

The example allows to update service account display name.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-set-display-name
        resource: gcp.service-account
        filters:
          - type: value
            key: name
            value: projects/{project}/serviceAccounts/{acountid}
        actions:
          - type: set-display-name
            display_name: test-name