Bucket - Update content type for filtered object
================================================

The example allows to update content type for filtered object.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-update-content-type
        resource: gcp.bucket-object
        filters:
          - type: value
            key: name
            value: object_name
        actions:
          - type: update-content-type
            content_type: image/png