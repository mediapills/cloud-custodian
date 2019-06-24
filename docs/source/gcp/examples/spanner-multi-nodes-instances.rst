Spanner - Report Multi-nodes Instances
================================

In GCP, Cloud Spanner is a managed relational database service which is globally consistent and scalable, intented for use in mission -critical applications. Teams may need to track consumption of Spanner resources thoroughly in order to stay in budget.

In the example below, the policy reports instances with 'nodes count' greater than or equal to 2.

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.


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
