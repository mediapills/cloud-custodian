Dataflow - Example 1
=======================

The example shows how to notify to Cloud Pub/Sub information about {details} ....

Details about all available kubernetes resources are available at the :ref:`gcp_dataflow` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-dataflow-job-notify
          description: |
            {description}
          resource: gcp.dataflow-job
          filters: {filters}
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dataflow