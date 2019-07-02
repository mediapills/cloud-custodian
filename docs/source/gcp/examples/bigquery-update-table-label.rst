BigQuery - Update filtered Table labels
=======================================

The example allows to delete filtered table.

.. code-block:: yaml

    policies:
      - name: gcp-bq-table-delete
        resource: gcp.bq-table
        filters:
          - type: value
            key: id
            value: new-project-26240:dataset.test
        actions:
          - type: update-table-label
            labels:
                - key: example
                  value: example
                - key: example1
                  value: example1