ML Engine Jobs - Set Labels 
==============================

Cloud infrastructure for enterprise corporation have a lot of components and one of the tool what can be used to group this components depends on needs is Labels.

In the example below, Custodian will set label "type" value "new" for ML Job after creation.

.. code-block:: yaml

    policies:
      - name: ml-job-set-labels
        resource: gcp.ml-job
        filters:
          - type: value
            key: jobId
            value: test_job
        actions:
          - type: set
            labels:
              - key: type
                value: new
