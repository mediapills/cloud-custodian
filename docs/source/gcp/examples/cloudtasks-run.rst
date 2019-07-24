Cloud Tasks - Delete Inappropriate Tasks
========================================

GCP Cloud Task is a unit of scheduled work.

The policy below makes Custodian to delete all Cloud Tasks that are scheduled in 7 or more days from now.

.. code-block:: yaml

    vars:
      deadline: &max_days_to_deadline 7

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
          - type: delete
