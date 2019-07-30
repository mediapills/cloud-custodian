ML Engine Model - Update description
====================================

Description management for ML Engine Models was not implemented via GCP Console. This example show how to change description for particular model in ML Engine.

In the example below, Custodian will change description for test model.

.. code-block:: yaml

    policies:
      - name: ml-model-update-description
        resource: gcp.ml-model
        filters:
          - type: value
            key: name
            value: projects/cloud-custodian/models/test
        actions:
          - type: set
            description: "Custom description"
