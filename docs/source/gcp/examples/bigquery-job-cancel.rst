BigQuery - Cancel job filtered job
================================

The example allows to delete filtered job.

.. code-block:: yaml

    policies:
      - name: gcp-big-jobs-cancel
        resource: gcp.bq-job
        filters:
          - type: value
            key: jobReference.jobId
            value: jobId
        actions:
          - type: cancel