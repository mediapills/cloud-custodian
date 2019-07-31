Storage - Audit Sensitive Buckets for Changes
=============================================

Buckets are the basic containers that hold data in Cloud Storage, everything must be contained in a bucket. Custodian can audit metadata of buckets including their ACLs and report any suspicious activity - e.g., if 'update' or 'patch' operations were performed either via GCP Concole, API or shell.

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies users if the ``update`` action was performed on buckets with 'archive' label.

.. code-block:: yaml

    policies:
      - name: gcp-storage-update
        resource: gcp.bucket
        mode:
          type: gcp-audit
          methods:
            - 'storage.buckets.update'
        filters:
          - type: value
            key: labels.key
            op: eq
            value: "archive"
        actions:
          - type: notify
            to:
              - email@address
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/storage
