.. _gcp_cloudiot:

Cloud IoT
=========

Filters
-------
 - Standard Value Filter (see :ref:`filters`)

Actions
-------
 - GCP Actions (see :ref:`gcp_genericgcpactions`)

Environment variables
---------------------
To check the policies please make sure that following environment variables are set:

- GOOGLE_CLOUD_PROJECT

- GOOGLE_APPLICATION_CREDENTIALS

The details about the variables are available in the `GCP documentation to configure credentials for service accounts. <https://cloud.google.com/docs/authentication/getting-started>`_

Example Policies
----------------

Cloud IoT. Device Registries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `device registries <https://cloud.google.com/iot/docs/reference/cloudiot/rest/v1/projects.locations.registries>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-cloudiot-registries-notify
          description: |
            Cloud IoT. List of device registries
          resource: gcp.cloudiot-registry
          query: # asia-east1, europe-west1, us-central1 are valid locations as of 2019-05-24
            - location: us-central1
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iot

Cloud IoT. Devices
~~~~~~~~~~~~~~~~~~
The resource works with `devices <https://cloud.google.com/iot/docs/reference/cloudiot/rest/v1/projects.locations.registries.devices>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-cloudiot-devices-notify
          description: |
            Cloud IoT. List of devices
          resource: gcp.cloudiot-device
          query: # asia-east1, europe-west1, us-central1 are valid locations as of 2019-05-24
            - location: us-central1
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/iot
