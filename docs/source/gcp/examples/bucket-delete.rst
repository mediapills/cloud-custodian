Storage - Delete Obsolete Buckets
================================

This sample policy deletes buckets that are updated more than 365 days ago.

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
