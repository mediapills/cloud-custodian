.. _gcp_storage:

Storage
========

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

Storage. Bucket Access Controls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `bucket access controls <https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-storage-bucket-access-controls-notify
          description: |
            Storage. List of bucket access controls
          resource: gcp.bucket-access-control
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/storage

Storage. Buckets
~~~~~~~~~~~~~~~~~
The resource works with `buckets <https://cloud.google.com/storage/docs/json_api/v1/buckets>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-storage-buckets-notify
          description: |
            Storage. List of buckets
          resource: gcp.bucket
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/storage

Storage. Default Object Access Controls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `default object access controls <https://cloud.google.com/storage/docs/json_api/v1/defaultObjectAccessControls>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-storage-default-object-access-controls-notify
          description: |
            Storage. List of bucket default object access controls
          resource: gcp.bucket-default-object-access-control
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/storage

Storage. Objects
~~~~~~~~~~~~~~~~~
The resource works with `objects <https://cloud.google.com/storage/docs/json_api/v1/objects>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-storage-bucket-objects-notify
          description: |
            Storage. List of bucket objects
          resource: gcp.bucket-object
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/storage
