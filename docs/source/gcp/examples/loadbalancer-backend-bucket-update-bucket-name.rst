Load Balancer - Backend buckets - Update bucket name
=====================================================

If backend buckets should be replaced into another bucket the example allows to do it.

.. code-block:: yaml

    policies:
      - name: gcp-loadbalancer-backend-buckets-patch-bucket-name
        resource: gcp.loadbalancer-backend-bucket
        filters:
          - type: value
            key: bucketName
            op: eq
            value: bucket-0
        actions:
          - type: set
            bucketName: bucket-1
