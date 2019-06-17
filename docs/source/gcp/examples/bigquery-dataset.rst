Big Query - Audit Creations of New Datasets
============================================

In Big Query, dataset is container for tables. Custodian can audit creations of new datasets which may be required for compliance reasons. 

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy watches for ``datasetservice.insert`` action in logs and notifies users if a new dataset was created in a non-default location, e.g. EU.  

.. code-block:: yaml

    policies:
        - name: gcp-big-query-audit-new-dataset
          resource: gcp.bq-dataset
          mode:
            type: gcp-audit
            methods:
            - "datasetservice.insert"
            filters:
            - type: value
              key: location
              op: equal
              value: EU
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query
