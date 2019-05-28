Dialogflow - Find by event name
================================

It described below how to notify to Cloud Pub\Sub information about intents that have 'WELCOME' event.

Details about all available Dialogflow resources are available at the :ref:`gcp_dialogflow` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: dialogflow-intents
          description: |
            Dialogflow. List of Intents with 'WELCOME' event
          resource: gcp.dialogflow-intent
          filters:
          - type: value
            key: events
            value: WELCOME
            op: contains
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dialogflow
