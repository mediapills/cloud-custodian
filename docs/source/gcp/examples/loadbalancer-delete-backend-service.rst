Load Balancer - Delete Backend Services without Backend
=======================================================

The example allows to delete backend services that don't have backends.

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
