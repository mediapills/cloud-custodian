.. _gcp_servicemanagement:

Service Management
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

Service Management. Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `service <https://cloud.google.com/service-infrastructure/docs/service-management/reference/rest/v1/services>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-service-management-services-notify
          description: |
            Storage. List of services in service management
          resource: gcp.service
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/service
