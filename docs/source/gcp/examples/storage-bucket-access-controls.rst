Storage - Watch for Changes in ACLs of Buckets
===============================================

Custodian can audit Access Control Lists (ACLs) of buckets - e.g., if 'update' or 'patch' operations were performed either via GCP Console, API or shell - and then stop and report such a suspicious activity.

Custodian can't reverse ACL permissions back to its previous state but can just remove new ACL asap and therefore reduce probability of potential data leakage, etc. 

This sample policy watches for 'update' action that sets OWNER role to all users. Upon such an event the policy automatically deletes the updated BucketAccessControl records (ACLs).

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
            op: in
            value: [allUsers, allAuthenticatedUsers]
          - type: value
            key: role
            op: eq
            value: OWNER
        actions:
          - type: delete
          - type: notify
            subject: suspicious change in ACL of buckets
            to:
              - email@address
            format: txt
            transport:
              type: pubsub
              topic: projects/my-gcp-project/topics/my-topic
