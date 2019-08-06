IAM - Update Service Account Descriptions
=============================================

Custodian can perform a mass update on all service accounts that match its filter.

The policy below updates descriptions of the filtered service accounts with new value.

.. code-block:: yaml

    policies:
      - name: gcp-iam-service-account-set
        resource: gcp.service-account
        filters:
          - type: value
            key: email
            op: in
            value: [sample1@email, sample2@email, sample3@email]
        actions:
          - type: set
            description: checked by Custodian
