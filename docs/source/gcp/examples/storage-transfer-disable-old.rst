Storage Transfer - Disable Old Storage Tranfer Jobs
===================================================

It is a good practice to control all active jobs and keep them actual.

The following policy disables active storage transfers (if any) which were created more than 365 days ago.

.. code-block:: yaml

    policies:
      - name: gke-cloud-storage-transfer-set
        resource: gcp.st-transfer-job
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
