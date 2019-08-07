BigQuery - Update filtered Dataset
==================================

The example allows set tableExpirationMs and labels for them.

.. code-block:: yaml

    policies:
      - name: gcp-big-dataset-set
        resource: gcp.bq-dataset
        filters:
          - type: value
            key: location
            value: US
        actions:
          - type: set
            tableExpirationMs: 7200000
            labels:
              - key: updated
                value: tableexparation