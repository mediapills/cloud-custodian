BigQuery - Delete filtered Datasets
===================================

The example allows to delete filtered datasets with set labels.

.. code-block:: yaml

    policies:
      - name: gcp-big-dataset-delete
        resource: gcp.bq-dataset
        filters:
          - type: value
            key: tag:updated
            value: tableexparation
        actions:
          - type: delete