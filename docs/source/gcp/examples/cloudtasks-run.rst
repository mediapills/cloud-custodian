Cloud Tasks - Notify if there are Tasks scheduled outside of planned operation period
=====================================================================================

Custodian can send notifications if there are Cloud Tasks scheduled in more than specified number of days from today.

Details about all available Cloud Tasks resources are available at the :ref:`gcp_cloudtasks` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    vars:
      deadline: &max_days_to_deadline 15

    policies:
      - name: gcp-cloudtasks-task-audit-run
        resource: gcp.cloudtasks-task
        filters:
          - type: value
            key: scheduleTime
            value_type: expiration
            value: *max_days_to_deadline
            op: ge
        actions:
          - type: notify
            to:
              - email@email
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/cloudtasks
