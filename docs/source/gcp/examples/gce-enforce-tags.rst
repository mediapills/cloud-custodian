Compute Engine - Enforce Instance Tags
======================================

Custodian can make sure VM Instances have particular tags applicable to VPC Firewall Rules.

In the example below, the policy adds the `tag-to-add-one`, `tag-to-add-two` tags to and removes the `tag-to-remove` tag from the instances that already have the `present-tag` tag.

.. code-block:: yaml

    policies:
      - name: gce-compute-enforce-tags
        resource: gcp.instance
        filters:
          - type: value
            key: tags.items[]
            op: in
            value_type: swap
            value: present-tag
        actions:
          - type: enforce-tags
            add-tags:
              - tag-to-add-one
              - tag-to-add-two
            remove-tags:
              - tag-to-remove
