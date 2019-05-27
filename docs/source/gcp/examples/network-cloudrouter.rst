Network - Check if there are unattached Cloud Routers
============================================================
Custodian can check and notify if there are unused (unattached) Cloud Routers. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy is set to filter routers which don't have any attached interface.

.. code-block:: yaml

    policies:
      - name: gcp-network-unattached-routers
        description: Checks unattached Cloud Routers
        resource: gcp.router
        filters:
           - type: value
             key: interfaces
             value: absent
        actions:
           - type: notify
             subject: Unattached Cloud Routers
             to:
               - email@address
             format: txt
             transport:
               type: pubsub
               topic: projects/my-gcp-project/topics/my-topic