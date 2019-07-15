Load Balancer - Delete HTTP/HTTPs health checks
==========================================

The policies allow to delete HTTP and HTTPs health checks for feature environments.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-update-https-health-checks
        resource: gcp.loadbalancer-https-health-check
        filters:
          - type: value
            key: host
            op: contains
            value: -dev-
        actions:
          - type: delete
      - name: gcp-loadbalancer-update-http-health-checks
        resource: gcp.loadbalancer-http-health-check
        filters:
          - type: value
            key: host
            op: contains
            value: -dev-
        actions:
          - type: delete
