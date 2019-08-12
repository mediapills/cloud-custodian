Pub/Sub - Set IAM Policies
==========================

Custodian can ensure that your Pub/Sub resources have an approved and controlled set of permissions.

This sample policy updates the IAM policy for Pub/Sub Topics whose name starts with `custodian-`.

.. code-block:: yaml

    policies:
      - name: gcp-pubsub-topic-set-iam-policy
        resource: gcp.pubsub-topic
        filters:
          - type: value
            key: name
            op: regex
            value: projects/your-project/topics/custodian-.*
        actions:
          - type: set-iam-policy
            add-bindings:
              - members:
                  - user:user1@test.com
                  - user:user2@test.com
                role: roles/editor
            remove-bindings:
              - members: "*"
                role: roles/owner
