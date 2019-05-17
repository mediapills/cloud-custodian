.. _gcp_iam:

Identity and Access Management
==============================

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

IAM. Project Roles
~~~~~~~~~~~~~~~~~~~
The resource works with `project roles <https://cloud.google.com/iam/reference/rest/v1/projects.roles>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-iam-project-roles-notify
          description: |
            IAM. List of project roles
          resource: gcp.project-role
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iam

IAM. Roles
~~~~~~~~~~~
The resource works with `roles <https://cloud.google.com/iam/reference/rest/v1/roles>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-iam-roles-notify
          description: |
            IAM. List of roles
          resource: gcp.iam-role
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iam

IAM. Service Accounts
~~~~~~~~~~~~~~~~~~~~~~
The resource works with `service accounts <https://cloud.google.com/iam/reference/rest/v1/projects.serviceAccounts>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-iam-roles-notify
          description: |
            IAM. List of service accounts
          resource: gcp.service-account
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iam
