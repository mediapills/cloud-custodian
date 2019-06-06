Compute Engine - Check Autoscaler target CPU utilization
========================================================
Custodian can check and notify if CPU scaling factor is lower than a target value. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy checks if there are autoscalers that target less than ``60%`` CPU utilization.

.. code-block:: yaml

    vars:
      min-utilization-target: &min-utilization-target 0.6

    policies:
        - name: gcp-gce-autoscalers
          resource: gcp.gce-autoscaler
          filters:
            - type: value
              key: autoscalingPolicy.cpuUtilization.utilizationTarget
              op: less-than
              value: *min-utilization-target
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/gce
