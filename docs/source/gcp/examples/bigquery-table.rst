Big Query - Warn on Upcoming Expiration of Tables
============================================

In Big Query, tables may have an expiration time upon which they will be deleted and their storage reclaimed. Custodian can check and notify if there are tables which are about to expire. 

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy checks if there are any tables labeled as "production:true"  which expires in 30 days or less.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-notify-bq-table
          resource: gcp.bq-table
          filters:
            - type: value
              key: 'tag:production'
              value: 'true'
            - type: value
              key: expirationTime
              op: less-than
              value-type: age
              value: 30
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query
