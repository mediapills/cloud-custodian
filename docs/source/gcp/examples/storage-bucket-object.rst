Storage - Audit bucket object changes
======================================

Custodian can audit bucket changes (e.g. a new file has been deployed). Note that the ``notify`` action requires a Pub/Sub topic to be configured.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies users if the ``update`` action appears in the logs.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-update
        resource: gcp.bucket-object
        mode:
          type: gcp-audit
          methods:
          - "storage.objects.update"
        actions:
          - type: notify
            to:
              - email@address
            format: json
            transport:
              type: pubsub
              topic: projects/cloud-custodian/topics/storage