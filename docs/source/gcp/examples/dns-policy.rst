DNS - Notify if logging is disabled in DNS Policy
=================================================

Custodian can check logging state in DNS Policy.

Details about all available DNS resources are available at the :ref:`gcp_dns` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-dns-policies-notify-if-logging-disabled
          resource: gcp.dns-policy
          filters:
            - type: value
              key: enableLogging
              value: false
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dns