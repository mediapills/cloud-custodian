.. _gcp_kms:

Key Management Service
=======================

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

KMS. Locations
~~~~~~~~~~~~~~~
The resource works with `locations <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-kms-location-notify
          description: |
            KMS. List of project locations
          resource: gcp.kms-location
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kms

KMS. Key Rings
~~~~~~~~~~~~~~~
The resource works with `key rings <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-kms-key-ring-notify
          description: |
            KMS. List of project key rings
          resource: gcp.kms-keyring
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kms

KMS. Crypto Keys
~~~~~~~~~~~~~~~~~
The resource works with `crypto keys <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-kms-key-ring-notify
          description: |
            KMS. List of project crypto keys
          resource: gcp.kms-cryptokey
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kms

KMS. Crypto Keys Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `crypto keys versions <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-crypto-key-version-notify
          description: |
            KMS. List of project crypto keys versions
          resource: gcp.kms-keyring
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kms
