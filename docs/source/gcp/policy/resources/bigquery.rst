.. _gcp_bigquery:

Big Query
==========

Filters
--------
 - Standard Value Filter (see :ref:`filters`)

Actions
--------
 - GCP Actions (see :ref:`gcp_genericgcpactions`)

Environment variables
---------------------
To check the policies please make sure that following environment variables are set:

- GOOGLE_CLOUD_PROJECT

- GOOGLE_APPLICATION_CREDENTIALS

The details about the variables are available in the `GCP documentation to configure credentials for service accounts. <https://cloud.google.com/docs/authentication/getting-started>`_

Example Policies
----------------

Big Query. Datasets
~~~~~~~~~~~~~~~~~~~
The resource works with `datasets <https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-datasets-notify
          description: |
            Big Query. List of Datasets
          resource: gcp.bq-dataset
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query

Big Query. Jobs
~~~~~~~~~~~~~~~~
The resource works with `jobs <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-jobs-notify
          description: |
            Big Query. List of Jobs
          resource: gcp.bq-job
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query

Big Query. Projects
~~~~~~~~~~~~~~~~~~~
The resource works with `projects <https://cloud.google.com/bigquery/docs/reference/rest/v2/projects>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-projects-notify
          description: |
            Big Query. List of Projects
          resource: gcp.bq-project
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query


Big Query. Tables
~~~~~~~~~~~~~~~~~~~
The resource works with `tables <https://cloud.google.com/bigquery/docs/reference/rest/v2/tables>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-big-query-tables-notify
          description: |
            Big Query. List of Tables
          resource: gcp.bq-table
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/big-query
