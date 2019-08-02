Bucket - Delete filtered bucket
===============================

The example allows to delete filtered bucket.
The following example demonstrates ability of Cloud Custodian to track buckets lifetime and 
delete buckets (if any) updated more than 365 days ago.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-delete
        resource: gcp.bucket
        filters:
          - type: value
            key: updated
            op: greater-than
            value_type: age
            value: 365
        actions:
          - type: delete
