Storage - Delete Obsolete Objects
=======================================

This sample policy deletes all objects older than 31 days in the buckets whose name matches the regular expression.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-delete
        resource: gcp.bucket-object
        filters:
          - type: value  
            key: bucket
            op: regexp
            value: ^archive[a-zA-Z0-9]+$
          - type: value
            key: timeCreated
            op: greater-than
            value_type: age
            value: 31
        actions:
          - type: delete
