Compute Engine - Check Security Policy
======================================
Custodian can check and notify if Compute Engine Security Policy is mis-configured. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy checks that there is only one rule allowing all connections.

.. code-block:: yaml

    policies:
      - name: gce-security-policy
        resource: gcp.gce-security-policy
        filters:
          - and:
              - type: value
                key: length(rules[])
                value: 1
              - type: value
                key: rules[].action
                op: in
                value: allow
                value_type: swap
              - type: value
                key: rules[].match.config.srcIpRanges[]
                op: in
                value: '*'
                value_type: swap
              - type: value
                key: rules[].priority
                op: in
                value: 2147483647
                value_type: swap
        actions:
          - type: notify
             to:
               - email@address
             format: txt
             transport:
               type: pubsub
               topic: projects/my-gcp-project/topics/my-topic
