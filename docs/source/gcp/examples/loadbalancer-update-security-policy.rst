Load Balancer - Set Security Policy
====================================

It's possible to update security policy for appropriate backend services.

.. code-block:: yaml

        policies:
        - name: gcp-loadbalancer-backend-service-set-security-policy
          resource: gcp.loadbalancer-backend-service
          filters:
          - type: value
            key: securityPolicy
            op: contains
            value: security-policy-0
          actions:
          - type: set-security-policy
            security-policy: security-policy-1
