Load Balancer - Delete Unsecured Forwarding Rules
==================================================

The example shows how to delete regional and global forwarding rules
that use portRange different from 443-443.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-forwarding-rules-delete
        resource: gcp.loadbalancer-forwarding-rule
        filters:
          - type: value
            key: portRange
            op: ni,
            value: [443-443]
        actions:
          - type: delete

      - name: gcp-loadbalancer-global-forwarding-rules-delete
        resource: gcp.loadbalancer-global-forwarding-rule
        filters:
          - type: value
            key: portRange
            op: ni,
            value: [443-443]
        actions:
          - type: delete