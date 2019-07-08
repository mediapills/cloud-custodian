Load Balancer - Delete Unsecured Forwarding Rules
==================================================

The example shows how to delete forwarding rules that use portRange different from 443-443.

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
