.. _gcp_dns:

DNS
====

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

DNS. Managed Zones
~~~~~~~~~~~~~~~~~~~
The resource works with `managed zones <https://cloud.google.com/dns/docs/reference/v1beta2/managedZones>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-dns-managed-zones-notify
          description: |
            DNS. List of DNS managed zones
          resource: gcp.dns-managed-zone
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dns

DNS. Policies
~~~~~~~~~~~~~~
The resource works with `policies <https://cloud.google.com/dns/docs/reference/v1beta2/policies>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name: gcp-dns-policies-notify
          description: |
            DNS. List of DNS policies
          resource: gcp.dns-policy
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dns