.. _gcp_machinelearning:

Machine Learning
=================

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

Machine Learning. Model
~~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `models <https://cloud.google.com/ml-engine/reference/rest/v1/projects.models>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-ml-models-notify
          description: |
            Machine Learning. List of models
          resource: gcp.ml-model
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/machine-learning

Machine Learning. Jobs
~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `jobs <https://cloud.google.com/ml-engine/reference/rest/v1/projects.jobs>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-ml-jobs-notify
          description: |
            Machine Learning. List of jobs
          resource: gcp.ml-jobs
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/machine-learning
