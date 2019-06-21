Load Balancer - Addresses
==========================

This example shows how to delete addresses with standard tiers.

.. code-block:: yaml

    policies:
        - name: load-balancers-addresses-in-standard-network-tier
          description: |
            Delete Load Balancers Addresses with standard network tier
          resource: gcp.loadbalancer-address
          filters:
            - type: value
              key: networkTier
              value: STANDARD
              op: eq
          actions:
            - type: delete
