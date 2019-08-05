Bucket - Update role for filtered entity
========================================

The example allows to update role for filtered entity.
It can be used for few resources like

- bucket-access-control,
- bucket-default-object-access-control,
- bucket-object-access-control

.. code-block:: yaml

    vars:
      entities-to-update: &entities-to-update
        - entity-name-1
        - entity-name-2
    policies:
      - name: gcp-bucket-access-control-update-role
        resource: gcp.bucket-access-control
        filters:
          - type: value
            key: entity
            op: in
            value: *entities-to-update
        actions:
          - type: set
            role: OWNER
