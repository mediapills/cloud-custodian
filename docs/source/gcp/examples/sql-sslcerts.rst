Cloud SQL - Notify on Certificates Which Are About to Expire
============================================================

In the example below, Cusodian tracks SSL certificates which are in use by Cloud SQL instances
and notify about the ones which are going to be expired in 60 days or less.

.. code-block:: yaml

    policies:
      - name: sql-ssl-cert
        description: |
          checks Cloud SQL filter on SSL certificates:
          returns certs which are about to expire in 60 days or less
        resource: gcp.sql-ssl-cert
        filters:
          - type: value
            key: expirationTime
            op: less-than
            value_type: expiration
            value: 60
        actions:
          - type: notify
            to:
              - email@address
            format: txt
            transport:
              type: pubsub
              topic: projects/my-project/topics/my-topic
