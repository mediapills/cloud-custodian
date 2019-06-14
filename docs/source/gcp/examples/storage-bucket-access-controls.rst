Storage - Watch Buckets for Changes in Access Control Lists
===============================================

Custodian can audit metadata of buckets including their ACLs and report any suspicious activity - e.g., if 'update' or 'patch' operations were performed either via GCP Concole, API or shell. 

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies users if the ``update`` action on buckets with 'production' label appears in the logs.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-access-control-update
        resource: gcp.bucket-access-control
        mode:
          type: gcp-audit
          methods:
          - "storage.objects.update"
          filters:
          - type: value
          - key: labels.key
          - value: "production"
        actions:
          - type: notify
            to:
              - email@address
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/storage
