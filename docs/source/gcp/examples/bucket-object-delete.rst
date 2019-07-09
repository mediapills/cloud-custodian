Bucket - Delete filtered object
===============================

The example allows to delete filtered object.

.. code-block:: yaml

     policies:
      - name: gcp-bucket-object-delete
        resource: gcp.bucket-object
        filters:
          - type: value
            key: name
            value: object_name
        actions:
          - type: delete