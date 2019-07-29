Bucket - Update storage class for filtered bucket
=================================================

The example allows to delete filtered bucket.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-update-storage-class
        resource: gcp.bucket
        filters:
          - type: value
            key: id
            value: bucket_name
        actions:
          - type: set
            class: MULTI_REGIONAL
