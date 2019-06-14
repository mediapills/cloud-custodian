Storage - Watch for Changes in ACLs of Buckets
===============================================

Custodian can audit Access Control Lists (ACLs) of buckets and report any suspicious activity - e.g., if 'update' or 'patch' operations were performed either via GCP Concole, API or shell. 

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies if the ``update`` action was performed on all bucket ACLs of the G Suite for Business domain example.com having 'OWNER' role.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-access-controls-update
        resource: gcp.bucket-access-control
        mode:
          type: gcp-audit
          methods:
          - "storage.BucketAccessControls.update"
          filters:
          - type: value
            key: entity
            op: eq
            value: "domain-example.com" 
          - type: value
            key: role
            op: eq
            value: "OWNER"
        actions:
          - type: notify
            to:
              - email@address
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/storage
