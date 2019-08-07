BigQuery - Mark all tables with expiration
==========================================

The example allows add labels to all tables which have
less than 7 days to expiration.

.. code-block:: yaml

    policies:
      - name: gcp-bq-table-delete
        resource: gcp.bq-table
        filters:
          - type: value
            key: expirationTime
            value_type: expiration
            op: less-than
            value: 7
        actions:
          - type: set
            expirationTime: 3600000
            labels:
              - key: expiration
                value: less_than_seven_days
