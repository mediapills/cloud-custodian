BigQuerydatatransfer - Delete Failed Transfer Configs
=====================================================

Custodian can check and delete all BigQuerydatatransfer Transfer Configs Failed during execution. During scheduled data transfer execution some of data sources can be out to data in this case you can just remove data transfer config like this.

In the example below, the policy checks if data transfer FAILED and delete all BigQuery data transfer configs matching this condition.

.. code-block:: yaml

    policies:
      - name: bq-datatransfer-delete-failed
        resource: gcp.bq-datatransfer
        filters:
          - type: value
            key: state
            value: FAILED
        actions:
          - type: delete
