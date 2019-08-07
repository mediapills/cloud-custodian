Storage Transfer - Disable Old Storage Tranfer Jobs
===================================================

It's a good practice to control all active jobs and remove obsolete ones.

The following policy disables active storage transfers (if any) which were created 
more than 365 days ago and notifies end users about this.

.. code-block:: yaml

    policies:
      - name: storage-transfer-transfer-job-set-and-notify
        resource: gcp.storagetransfer-transfer-job
        filters:
          - type: value
            key: creationTime
            op: greater-than
            value_type: age
            value: 365
        actions:
          - type: set
            status: DISABLED
          - type: notify
            to:
              - email@address
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/storage-transfer
