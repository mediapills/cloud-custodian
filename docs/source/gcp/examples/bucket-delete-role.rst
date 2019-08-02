Bucket - Delete filtered role for buckets
=========================================

The example allows to delete bucket access control based on filtered roles for buckets.
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
        actions:
          - type: delete
