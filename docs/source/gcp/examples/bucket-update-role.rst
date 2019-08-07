Storage - Enforce Role for Chosen Permission Holders
====================================================

The BucketAccessControls resource represents the Access Control Lists (ACLs) for buckets within Google Cloud Storage. ACLs let you specify who has access to your data and to what extent. Refer to GCP documentation for more details.

The policy below updates all BucketAccessControls of the listed IAM entities (permission holders - user, group, domain, etc) and assigns them 'reader' role. 

This operation can be done for several GCP resources:

- bucket-access-control,
- bucket-default-object-access-control,
- bucket-object-access-control

.. code-block:: yaml

    vars:
      entities-to-update: &entities-to-update
        - entity-name-1
        - entity-name-2
    policies:
      - name: gcp-bucket-access-control-update-role
        resource: gcp.bucket-access-control
        filters:
          - type: value
            key: entity
            op: in
            value: *entities-to-update
        actions:
          - type: set
            role: READER
