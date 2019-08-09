Load Balancer - Delete Backend Services without Backend
=======================================================

This sample policy deletes backend services that don't have backends.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-backend-service-delete
        resource: gcp.loadbalancer-backend-service
        filters:
          - type: value
            key: backends
            value: absent
        actions:
          - type: delete
