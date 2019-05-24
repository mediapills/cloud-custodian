Big Query - Dataset creation
============================================

Custodian can audit dataset creation. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy notifies users if the ``datasetservice.insert`` action appears in the logs.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-audit-new-dataset
          resource: gcp.bq-dataset
          mode:
            type: gcp-audit
            methods:
            - "datasetservice.insert"
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query