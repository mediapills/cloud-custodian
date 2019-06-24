Load Balancer - URL Maps - Delete / Invalidate Cache
=====================================================

There are examples how to delete and invalidate cache of URL Maps by part of name.

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
        - name: gcp-loadbalancer-url-map-invalidate-cache
          resource: gcp.loadbalancer-url-map
          filters:
          - type: value
            key: name
            op: contains
            value: custodian
          actions:
          - type: invalidate-cache