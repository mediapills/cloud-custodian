Bucket - Delete filtered role for bucket
========================================

The example allows to filtered role for bucket.
It can be used for few resources like

- bucket-access-control,
- bucket-default-object-access-control,
- bucket-object-access-control

.. code-block:: yaml

    policies:
      - name: gcp-bucket-access-control-delete-role
        resource: gcp.bucket-access-control
        filters:
          - type: value
            key: role
            value: READER
          - type: value
            key: id
            value: bucket_name
        actions:
          - type: delete
