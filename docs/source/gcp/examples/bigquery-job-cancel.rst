BigQuery - Cancel all finished jobs
===================================

The example allows to cancel all finished jobs.

.. code-block:: yaml

    policies:
      - name: gcp-big-jobs-cancel
        resource: gcp.bq-job
        filters:
          - type: value
            key: state
            value: DONE
        actions:
          - type: cancel