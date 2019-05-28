.. _gcp_dialogflow:

Dialogflow
===========

Filters
--------
 - Standard Value Filter (see :ref:`filters`)

    Fields for filtering can be received from GCP resource object. Link to appropriate resource is provided in each GCP resource.

Actions
--------
 - GCP Actions (see :ref:`gcp_genericgcpactions`)

Example Policies
----------------

Dialogflow. Agents
~~~~~~~~~~~~~~~~~~~
`GCP resource: Agents <https://cloud.google.com/dialogflow-enterprise/docs/reference/rest/v2/Agent>`_

.. code-block:: yaml

    policies:
        - name: dialogflow-agents
          description: |
            Dialogflow. List of Agents
          resource: gcp.dialogflow-agent
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dialogflow

Dialogflow. Entity Types
~~~~~~~~~~~~~~~~~~~~~~~~~
`GCP resource: Entity Types <https://cloud.google.com/dialogflow-enterprise/docs/reference/rest/v2/projects.agent.entityTypes>`_

.. code-block:: yaml

    policies:
        - name: dialogflow-entity-types
          description: |
            Dialogflow. List of Entity types
          resource: gcp.dialogflow-entity-type
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dialogflow

Dialogflow. Intents
~~~~~~~~~~~~~~~~~~~~
`GCP resource: Intents <https://cloud.google.com/dialogflow-enterprise/docs/reference/rest/v2/projects.agent.intents>`_

.. code-block:: yaml

    policies:
        - name: dialogflow-intents
          description: |
            Dialogflow. List of Intents
          resource: gcp.dialogflow-intent
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dialogflow
