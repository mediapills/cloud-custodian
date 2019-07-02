BigQuery - Delete filtered Table
==================================

The example allows to delete filtered table.

.. code-block:: yaml

      policies:
        - name: gcp-big-table-delete
          resource: gcp.bq-table
          filters:
              - type: value
                key: id
                value: project_id:dataset_id.table_id
          actions:
            - type: delete