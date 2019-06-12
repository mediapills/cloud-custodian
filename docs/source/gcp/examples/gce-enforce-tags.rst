Compute Engine - Enforce Instance Tags
======================================

Custodian can make sure VM Instances have particular tags applicable to VPC Firewall Rules.

In the example below, the policy adds the `tags`, `you`, `want`, `to`, `enforce` tags to instances that already have the `target` tag.

These policies update the IAM policy for spanner instances (`add-bindings`) and databases (`remove-bindings`), respectively.

.. code-block:: yaml

    policies:
      - name: gce-compute-enforce-tags
        resource: gcp.instance
        filters:
          - type: value
            key: tags.items[]
            op: in
            value_type: swap
            value: target
        actions:
          - type: enforce-tags
            tags:
              - target
              - tags
              - you
              - want
              - to
              - enforce
