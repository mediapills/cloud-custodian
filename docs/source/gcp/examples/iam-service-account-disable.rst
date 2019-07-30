IAM - Disable Service Account
============================

The example allows to disable filtered service account.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-disable
        resource: gcp.service-account
        filters:
          - type: value
            key: name
            value: projects/{project}/serviceAccounts/{acountid}
        actions:
          - type: disable