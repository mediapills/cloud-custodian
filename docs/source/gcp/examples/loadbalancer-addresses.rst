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


This example shows how to delete addresses with '-dev-' suffix.

.. code-block:: yaml

    policies:
      - name: load-balancers-global-addresses-dev
        description: |
            Delete Load Balancers Global Addresses with dev suffix
        resource: gcp.loadbalancer-global-address
        filters:
          - type: value
            key: name
            value: -dev-
            op: contains
        actions:
          - type: delete
