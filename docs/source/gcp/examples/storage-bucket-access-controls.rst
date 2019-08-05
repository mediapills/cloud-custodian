Storage - Watch for Changes in ACLs of Buckets
===============================================

Custodian can audit Access Control Lists (ACLs) of buckets and report any suspicious activity - 
e.g., if 'update' or 'patch' operations were performed either via GCP Concole, API or shell.

In the example below, the policy `delete` action was performed on all bucket
ACLs of the G Suite for Business domain example.com having 'OWNER' role.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-access-controls-update
        resource: gcp.bucket-access-control
        mode:
          type: gcp-audit
          methods:
            - storage.BucketAccessControls.update
        filters:
          - type: value
            key: entity
            op: eq
            value: domain-example.com
          - type: value
            key: role
            op: eq
            value: OWNER
        actions:
          - type: delete

