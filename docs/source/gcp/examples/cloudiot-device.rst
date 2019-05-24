Cloud IoT - Check Devices not to be blocked
===========================================
Custodian can check if there are blocked IoT Devices. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy filters devices in the ``europe-west1`` location which must be specified in the ``query`` section.

.. code-block:: yaml

    policies:
        - name: gcp-cloudiot-device-audit-new
          resource: gcp.cloudiot-device
          filters:
            - type: value
              key: blocked
              value: true
          query:
            - location: europe-west1
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iot