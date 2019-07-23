Load Balancer - Update protocols in Backend Services
=====================================================

The example allows to replace protocols in the backend service.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-backend-service-update-protocol
        resource: gcp.loadbalancer-backend-update-protocol
        filters:
          - type: value
            key: protocol
            value: HTTP
        actions:
          - type: set
            protocol: HTTPS
