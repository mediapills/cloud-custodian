BigQuery - Delete filtered Tables
=================================

The example allows to delete all tables older than 31 days.

.. code-block:: yaml

      policies:
        - name: gcp-big-table-delete
          resource: gcp.bq-table
          filters:
            - type: value
              key: creationTime
              value_type: age
              op: greater-then
              value: 31
          actions:
            - type: delete