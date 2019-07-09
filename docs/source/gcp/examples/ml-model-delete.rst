ML Engine Model - Delete Action
===============================

It is a good practice for data science to control model live cycle. Training process can effect on model state and in nowadays dynamic models creation is common practice.

In the example below, after policy execution model will be deleted by name.

.. code-block:: yaml

    policies:
      - name: ml-model-delete
        resource: gcp.ml-model
        filters:
          - type: value
            key: name
            value: projects/cloud-custodian/models/test
        actions:
          - type: delete
