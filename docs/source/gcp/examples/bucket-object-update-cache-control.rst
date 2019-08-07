Bucket - Update cache controls for filtered objects
===================================================

The example allows to update cache controls for objects which are older than one year.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-set-cache-controls
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
