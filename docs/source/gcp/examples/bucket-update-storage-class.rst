Bucket - Update storage class by location
=========================================

The example allows to update filtered buckets by location and distribute them multi regionally.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-update-storage-class
        resource: gcp.bucket
        filters:
          - type: value
            key: location
            value: US
        actions:
          - type: set
            class: MULTI_REGIONAL
