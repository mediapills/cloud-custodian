Cloud SQL - Delete Backups Older Than N Days
============================================

The following example demonstrates ability of Cloud Custodian to track backup runs of Cloud SQL instances, delete backups (if any) older than 5 days and send a corresponding notification.

.. code-block:: yaml

    policies:
    - name: sql-backup-run
      description: |
          delete backups older than 5 days
      resource: gcp.sql-backup-run
      filters:
        - type: value
          key: endTime
          op: greater-than
          value_type: age
          value: 5
      actions:
        - type: delete
        - type: notify
          to:
            - email@address
          format: txt
          transport:
              type: pubsub
              topic: projects/my-project/topics/my-topic
