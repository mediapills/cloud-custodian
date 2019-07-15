Load Balancer - Update HTTP/HTTPs health checks
==========================================

The policies allow to update HTTP and HTTPs health checks for different environments.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-update-https-health-checks
        resource: gcp.loadbalancer-http-health-check
        filters:
          - type: value
            key: host
            op: contains
            value: -dev
        actions:
          - type: patch
            healthyThreshold: 2,
            host: cloudcustodian.com
            requestPath: /test
            port: 8080
            checkIntervalSec: 10
            timeoutSec: 9
            unhealthyThreshold: 10
      - name: gcp-loadbalancer-update-http-health-checks
        resource: gcp.loadbalancer-https-health-check
        filters:
          - type: value
            key: host
            op: contains
            value: -qa
        actions:
          - type: patch
            healthyThreshold: 1,
            host: cloudcustodian.com
            requestPath: /test
            port: 8081
            checkIntervalSec: 5
            timeoutSec: 3
            unhealthyThreshold: 5
