Spanner - Drop databases
=========================

The policy from the example allows to drop databases and notify about the action by an email.
The databases have `dev` in the name and can be used for dev environments.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
    - name: gcp-spanner-instance-databases-delete-and-notify
      resource: gcp.spanner-database-instance
      filters:
        - type: value
          key: name
          op: contains
          value: dev
      actions:
      - type: notify
        subject: The following databases were dropped
        to:
        - email@address
        transport:
          type: pubsub
          topic: projects/cloud-custodian/topics/demo-notifications
      - type: delete