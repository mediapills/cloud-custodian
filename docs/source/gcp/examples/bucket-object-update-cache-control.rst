Bucket - Update cache control for filtered objects
==================================================

The example allows to update cache control for objects which older than one year.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-update-content-type
        resource: gcp.bucket-object
        filters:
          - type: value
            key: updated
            op: greater-than
            value_type: age
            value: 365
        actions:
          - type: set
            cache_control: max-age=3600