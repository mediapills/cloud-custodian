Dataflow -  Check if any job has status done
=======================

Custodian can audit job changes. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy checks if there are any jobs has currentState ``JOB_STATE_DONE``.

.. code-block:: yaml

    policies:
      - name: gcp-dataflow-jobs-update
        resource: gcp.dataflow-job
        filters:
          - type: value
            key: currentState
            value: JOB_STATE_DONE
        actions:
          - type: notify
            to:
              - email@address
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/dataflow
