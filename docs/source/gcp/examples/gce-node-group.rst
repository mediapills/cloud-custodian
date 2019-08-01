Compute Engine - Delete Node Groups with Invalid Number of Nodes
================================================================

Custodian can delete Node Groups that have too many nodes.

In the example below, the policy checks if there are Node Groups whose ``size`` is greater than ``2``.

.. code-block:: yaml

    policies:
      - name: gcp-gce-node-group-delete-greater-than-2-nodes
        resource: gcp.gce-node-group
        filters:
          - type: value
            key: size
            op: greater-than
            value: 2
        actions:
          - type: delete
