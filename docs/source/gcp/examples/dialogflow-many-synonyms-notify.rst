Dialogflow - Notify about many synonyms
========================================

It described below how to notify to Cloud Pub\Sub information about entity types that have 2 or more synonyms.

Details about all available Dialogflow resources are available at the :ref:`gcp_dialogflow` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
    - name: dialogflow-entity-types
      description: |
            Dialogflow. List of Entity Types with more or equal 2 synonyms
      resource: gcp.dialogflow-entity-type
      filters:
      - type: value
        key: entities[].synonyms
        value: 2
        value_type: size
        op: gte
      actions:
      - type: notify
        to:
        - email@address
        format: json
        transport:
          type: pubsub
          topic: projects/cloud-custodian/topics/dialogflow
