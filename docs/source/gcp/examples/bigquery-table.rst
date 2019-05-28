Big Query - Check expiration date
============================================

Custodian can check and notify if there are user-defined job is done. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy checks if there are any tables closer to expiration date.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-notify-bq-table
          resource: gcp.bq-table
          filters:
              - type: value
                key: expirationTime
                op: less-than
                value: 60
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query
