Bucket - Update filtered bucket iam policy
==========================================

The example allows to update filtered bucket iam policy.

.. code-block:: yaml

    policies:
    - name: gcp-storage-bucket-set-iam-policy
      resource: gcp.bucket
      filters:
        - type: value
          key: id
          value: bucket_name
      actions:
      - type: set-iam-policy
        bindings:
        - members:
          - user:user1@test.com
          - user2@test.com
          role: roles/owner
        - members:
          - user:user3@gmail.com
          role: roles/viewer
