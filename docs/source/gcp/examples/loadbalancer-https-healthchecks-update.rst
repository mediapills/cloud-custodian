Load Balancer - Update HTTPs healthchecks
==========================================

# If a bucket was deleted it doesn't mean that appropriate backend buckets were deleted. The policy allow to delete backend buckets by the name of non-existing bucket.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-update-https-health-checks
        resource: gcp.loadbalancer-https-health-check
        filters:
          - type: value
            key: host
            op: eq
            value: custodian.com
        actions:
          - type: patch
            healthyThreshold: 2,
            host: cloudcustodian.com
            requestPath: /test
            port: 8080
            checkIntervalSec: 10
            timeoutSec: 9
            unhealthyThreshold: 10
