Storage Transfer - Disable Old Storage Tranfer Jobs
===================================================

It is a good practice to control all active jobs and keep them up-to-date.

The following policy disable active storage transfers (if any) which were created more than 365 days ago and notify end user about this.

.. code-block:: yaml

    policies:
      - name: storage-transfer-transfer-job-set
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
