Load Balancer - Set Security Policy
===================================

This sample policy updates security policy for backend services that match its filter.

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
