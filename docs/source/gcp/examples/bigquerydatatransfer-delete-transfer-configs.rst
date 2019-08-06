BigQuery Data Transfer - Delete Failed Transfer Configs
========================================================

Custodian can check and delete all BigQuery Transfer Configs which failed during execution for some reason (for example, during a scheduled data transfer some of data sources were out to date).

The policy below checks if data transfer status is FAILED and delete all such transfer configs.

.. code-block:: yaml

    policies:
      - name: bq-datatransfer-delete-failed
        resource: gcp.bq-datatransfer-transfer-config
        filters:
          - type: value
            key: state
            value: FAILED
        actions:
          - type: delete
