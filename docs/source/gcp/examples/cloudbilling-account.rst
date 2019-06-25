Cloud Billing - Audit Billing Accounts
===================================================

Custodian can watch for changes in a scope or configuration of billing accounts and report suspicious changes for additional check by responsible controller.

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

The policy below audits logs and notifies if new resources are assigned to any open billing account.

.. code-block:: yaml

    policies:
        - name: gcp-cloudbilling-account-audit-assigned
          resource: gcp.cloudbilling-account
          mode:
            type: gcp-audit
            methods:
              - "AssignResourceToBillingAccount"
            filters:
              - type: value
                key: open
                op: equal
                value: true
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/billing
