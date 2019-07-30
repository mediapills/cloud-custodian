IAM - Delete Service Account
============================

The example allows to delete filtered service account.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-delete
        resource: gcp.service-account
        filters:
          - type: value
            key: name
            value: projects/{project}/serviceAccounts/{acountid}
        actions:
          - type: delete