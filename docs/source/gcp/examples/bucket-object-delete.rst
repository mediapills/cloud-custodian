Storage - Delete Obsolete Objects
=======================================

This sample policy deletes all objects older than 31 days.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-delete
        resource: gcp.bucket-object
        filters:
          - type: value
            key: timeCreated
            op: greater-than
            value_type: age
            value: 31
        actions:
          - type: delete
