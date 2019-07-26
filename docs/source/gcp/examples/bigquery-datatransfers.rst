Big Query Data Transfer - Notify about Failed Transfer Configs
==============================================================

There is a possibility select BigQuerydatatransfer Transfer Configs Failed during execution. During scheduled data transfer execution some of data sources can be out to data in this case you can just remove data transfer config like this.

In the example below, the policy will notify about data transfer FAILS via email.

.. code-block:: yaml

    policies:
      - name: bq-datatransfer-delete-failed
        resource: gcp.bq-datatransfer
        filters:
          - type: value
            key: state
            value: FAILED
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/bdt
