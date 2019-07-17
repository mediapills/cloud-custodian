Spanner - Reduce count of instance nodes
=========================================

The policy from the example allows to reduce node count to 1 node for a spanner instance and notify about the action by an email.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
    - name: gcp-spanner-instances-change-node-count
      resource: gcp.spanner-instance
      filters:
        - type: value
          key: nodeCount
          op: gte
          value: 2
      actions:
      - type: set
        nodeCount: 1
