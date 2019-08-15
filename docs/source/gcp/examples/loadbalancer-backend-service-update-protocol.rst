Load Balancer - Update Protocols in Backend Services
====================================================

This sample policy replaces protocols in the backend service.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-backend-service-update-protocol
        resource: gcp.loadbalancer-backend-service
        filters:
          - type: value
            key: protocol
            value: HTTP
        actions:
          - type: set
            protocol: HTTPS
