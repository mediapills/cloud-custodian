Bucket - Delete filtered buckets
================================

The example allows to delete filtered buckets.
The following example demonstrates ability of Cloud Custodian to 
delete the buckets (if any) updated more than 365 days ago.

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
