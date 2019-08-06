Cloud SQL - Check Regions of Instances and Their States
=======================================================

Execution of the following policy returns instances which are not in an approved set of regions
AND not in a runnable state. You may use more complex logic to combine any conditions you need.

.. code-block:: yaml

    policies:
      - name: sql-instance
        description: |
          check basic work of Cloud SQL filter on instances: returns instances which are not in an approved set of regions AND not in runnable state
        resource: gcp.sql-instance
        filters:
          - type: value
            key: region
            op: not-in
            value: [europe-west1, europe-west2]
          - type: value
            key: state
            op: not-equal
            value: RUNNABLE
        actions:
          - type: notify
            to:
              - email@address
            format: txt
            transport:
              type: pubsub
              topic: projects/my-project/topics/my-topic
