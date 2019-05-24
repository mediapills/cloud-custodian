Cloud IoT - Audit Devices being added
=====================================

Custodian can audit and send notifications if an IoT Device is added to a Registry.

Details about all available Cloud IoT resources are available at the :ref:`gcp_cloudiot` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-cloudiot-device-audit-new
          resource: gcp.cloudiot-device
          mode:
            type: gcp-audit
            methods:
              - "google.cloud.iot.v1.DeviceManager.CreateDevice"
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iot