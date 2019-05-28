Dialogflow - Notify about agents with enabled logging
======================================================

It described below how to notify to Cloud Pub\Sub information about agents with enabled logging.

Details about all available Dialogflow resources are available at the :ref:`gcp_dialogflow` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: dialogflow-agents
          description: |
            Dialogflow. List of Agents with enabled logging
          resource: gcp.dialogflow-agent
          filters:
          - type: value
            key: enableLogging
            value: true
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dialogflow
