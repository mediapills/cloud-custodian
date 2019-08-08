Storage - Delete Inappropriate Permissions
==========================================

The BucketAccessControls resource represents the Access Control Lists (ACLs) for buckets within Google Cloud Storage. ACLs let you specify who has access to your data and to what extent. Refer to GCP documentation for more details.

Your organization security policies may prohibit to open access for non-authentiated users.

The policy below automaticaly deletes all BucketAccessControl that contain 'allUsers' record.
This operation can be done for several GCP resources:

- bucket-access-control,
- bucket-default-object-access-control,
- bucket-object-access-control

.. code-block:: yaml

    policies:
      - name: gcp-bucket-access-control-delete
        resource: gcp.bucket-access-control
        filters:
          - type: value
            key: role
            value: READER
        actions:
          - type: delete
