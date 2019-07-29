Storage - Watch Sensitive Objects for Changes
=============================================

Objects are pieces of data that are uploaded to Google Cloud Storage. Custodian can audit metadata of objects including their ACLs and report any suspicious activity - e.g., if 'update' or 'patch' operations were performed either via GCP Concole, API or shell.

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies users if the ``update`` action was performed on objects of ColdLine storage class.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-update
        resource: gcp.bucket-object
        mode:
          type: gcp-audit
          methods:
            - 'storage.objects.update'
            filters:
            - type: value
              key: storageClass
              op: eq
              value: "ColdLine"
        actions:
          - type: notify
            to:
              - email@address
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/storage
