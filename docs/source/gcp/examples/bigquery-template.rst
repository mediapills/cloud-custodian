Big Query - Template 1
============================================

TBD {Description}

Details about all available IAM resources are available at the :ref:`gcp_bigquery` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: {policy name}
          description: |
            {description}
          resource: {resource}
          filters: {filters}
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query