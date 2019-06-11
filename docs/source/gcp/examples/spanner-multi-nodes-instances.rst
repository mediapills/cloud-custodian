Spanner - Multi nodes instances
================================

These examples allow to work with GCP spanner resource. It describes below how to notify to Cloud Pub/Sub information about spanner instances with nodes count greater than 2.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-spanner-instances-notify
          description: |
            Spanner. List of multi nodes instances
          resource: gcp.spanner-instance
          filter:
            - type: value
              key: nodeCount
              op: gte
              value: 2
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/spanner