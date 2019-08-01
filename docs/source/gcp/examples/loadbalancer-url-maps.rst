Load Balancer - URL Maps - Delete
==================================

There is an example how to delete URL Maps by part of name.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-url-map-delete
        resource: gcp.loadbalancer-url-map
        filters:
          - type: value
            key: name
            op: contains
            value: url-map
        actions:
          - type: delete
