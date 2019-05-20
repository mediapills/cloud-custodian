Cloud Billing - Audit Billing Account being assigned to a resource
==================================================================

Custodian can audit and send notifications if a Billing Account is assigned to such resources as projects.

Details about all available Cloud Billing resources are available at the :ref:`gcp_cloudbilling` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-cloudbilling-account-audit-assigned
          resource: gcp.cloudbilling-account
          mode:
            type: gcp-audit
            methods:
              - "AssignResourceToBillingAccount"
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/billing