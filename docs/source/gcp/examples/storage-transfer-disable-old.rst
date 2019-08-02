Storage Transfer - Disable Old Storage Tranfer Jobs
===================================================

The example allows to update filtered storage transfers. The following example demonstrates ability of Cloud Custodian to disable active storage transfers by lifetime (if any) created more than 365 days ago.

.. code-block:: yaml

    policies:
      - name: gke-cloud-storage-transfer-set
        resource: gcp.st-transfer-job
        filters:
          - type: value
            key: status
            value: ENABLED
          - type: value
            key: creationTime
            op: greater-than
            value_type: age
            value: 365
        actions:
          - type: set
            status: DISABLED
