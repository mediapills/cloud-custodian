.. _gcp_deploymentmanager:

Deployment Manager
===================

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

DM. Deployments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `deployments <https://cloud.google.com/deployment-manager/docs/reference/latest/deployments>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-dm-deployments-notify
          description: |
            Deployment Manager. List of Deployments
          resource: gcp.dm-deployment
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/pubsub