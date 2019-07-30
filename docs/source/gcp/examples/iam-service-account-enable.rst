IAM - Enable Service Account
============================

The example allows to Enable filtered service account.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-enable
        resource: gcp.service-account
        filters:
          - type: value
            key: name
            value: projects/{project}/serviceAccounts/{acountid}
        actions:
          - type: enable