BigQuery - Delete filtered Dataset table expiration
===================================================

The example allows to delete filtered dataset.

.. code-block:: yaml

    policies:
        - name: gcp-big-dataset-delete
          resource: gcp.bq-dataset
          filters:
              - type: value
                key: id
                value: project_id:dataset_id
          actions:
              - type: delete