.. _gcp_vpc:

VPC
====

Filters
--------
 - Standard Value Filter (see :ref:`filters`)

    Fields for filtering can be received from GCP resource object. Link to appropriate resource is provided in each GCP resource.

Actions
--------
 - GCP Actions (see :ref:`gcp_genericgcpactions`)

Example Policies
----------------

VPC. Access Policy
~~~~~~~~~~~~~~~~~~~
`GCP resource: Access Policy <https://cloud.google.com/access-context-manager/docs/reference/rest/v1/accessPolicies>`_

.. code-block:: yaml

    policies:
        - name: all-vpc-access-policies
          description: |
            VPC. List of Access Policies
          resource: gcp.vpc-access-policy
          query:
            - organization_id: <organization_id>
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/vpc

VPC. Access Level
~~~~~~~~~~~~~~~~~~~
`GCP resource: Access Level <https://cloud.google.com/access-context-manager/docs/reference/rest/v1/accessPolicies.accessLevels>`_

.. code-block:: yaml

    policies:
        - name: all-vpc-access-levels
          description: |
            VPC. List of Access Levels
          resource: gcp.vpc-access-level
          query:
            - organization_id: <organization_id>
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/vpc

VPC. Service Perimeter
~~~~~~~~~~~~~~~~~~~~~~~
`GCP resource: Service Perimeter <https://cloud.google.com/access-context-manager/docs/reference/rest/v1/accessPolicies.servicePerimeters>`_

.. code-block:: yaml

    policies:
        - name: all-vpc-service-perimeters
          description: |
            VPC. List of Service Perimeters
          resource: gcp.vpc-service-perimeter
          query:
            - organization_id: <organization_id>
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/vpc
