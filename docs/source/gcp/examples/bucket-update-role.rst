Bucket - Update role for filtered entity
========================================

The example allows to update role for filtered entity.
It can be used for few resources like

- bucket-access-control,
- bucket-default-object-access-control,
- bucket-object-access-control

.. code-block:: yaml

    policies:
      - name: gcp-bucket-access-control-update-role
        resource: gcp.bucket-access-control
        filters:
          - type: value
            key: entity
            value: entity_name
        actions:
          - type: set
            role: OWNER
