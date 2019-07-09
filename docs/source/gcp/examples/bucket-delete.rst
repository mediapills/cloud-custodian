Bucket - Delete filtered bucket
===============================

The example allows to delete filtered bucket.

.. code-block:: yaml

     policies:
      - name: gcp-bucket-delete
        resource: gcp.bucket
        filters:
          - type: value
            key: id
            value: bucket_name
        actions:
          - type: delete