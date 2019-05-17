Deployment Manager - Template 1
================================

The Description

Details about all available Deployment Manager resources are available at the :ref:`gcp_deploymentmanager` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: name1
          description: |
            List of ....
          resource: gcp.dm-deployment
          filters:
            - type:
              key:
              value:
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/deployment-manager