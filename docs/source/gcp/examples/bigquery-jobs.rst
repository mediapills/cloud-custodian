Big Query - Check if job is done
============================================

Custodian can check and notify if there are user-defined job is done. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy checks if there are any jobs has status done.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-notify-if-job-done
          resource: gcp.bq-job
          filters:
            - type: value
              key: status.state
              value: DONE
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query
