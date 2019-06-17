Big Query - Check for Abnormally Long Queries
============================================

Once started, a job in the Big Query queries, loads, extracts or transforms data and then normally enters a terminal state. Custodian can check if there are any jobs which remain running abnormally long. 

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy checks if there are any jobs of ``QUERY`` type which started over 1 day ago (configurable period) but not yet transitioned to a stable state for some reason (remains in ``RUNNING`` status) and therefore may need administrator's attention.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-notify-if-job-done
          resource: gcp.bq-job
          filters:
            - type: value
              key: configuration.jobtype
              op: equal
              value: QUERY
            - type: value
              key: statistics.starttime
              op: greater-than
              value_type: age
              value: 1
            - type: value
              key: status.state
              op: equal
              value: RUNNING
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query
