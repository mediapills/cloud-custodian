Cloud IoT - Audit Device Registries being created
=================================================

Custodian can audit and send notifications if an IoT Device Registry is created.

Details about all available Cloud IoT resources are available at the :ref:`gcp_cloudiot` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-cloudiot-registry-audit-creation
          resource: gcp.cloudiot-registry
          mode:
            type: gcp-audit
            methods:
              - "google.cloud.iot.v1.DeviceManager.CreateDeviceRegistry"
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iot