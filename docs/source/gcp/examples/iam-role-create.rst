IAM - Watch for Creation of New Roles
============================================================

In GCP, role is collection of permissions which can be granted to a user, a group, or a service account. GCP also provides the ability to create customized Cloud IAM roles.

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

The following policy audits logs in real-time for traces of "CreateRole" action and will notify an admin and/or IT security manager about creation of new roles with "Generally Available" stage.

.. code-block:: yaml

    policies:
      - name: iam-role-policy
        description: |
          Notify IAM role created
        resource: gcp.project-role
        mode:
          type: gcp-audit
          methods:
          - "google.iam.admin.v1.CreateRole"
          filters:
          - type: value
            key: stage
            op: equal
            value: GA
        actions:
          - type: notify
            subject: IAM role has been created
            to:
              - Pub/Sub
            transport:
              type: pubsub
              topic: projects/mythic-tribute-232915/topics/iam-demo
