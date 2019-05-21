Storage - Example 1
====================

{Description}

Details about all available Storage resources are available at the :ref:`gcp_storage` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: {name}
          description: |
            {Description}
          resource: {resource name}
          filters: {filters}
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/storage