VPC - Find policies by service perimeters' options
===================================================

It described below how to notify to Cloud Pub\Sub information if Cloud Spanner API available in the service perimeter.

Details about all available VPC resources are available at the :ref:`gcp_vpc` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: vpc-service-perimeters
          description: |
            VPC. List of Service Perimeters
          resource: gcp.vpc-service-perimeter
          query:
            - organization_id: <organization_id>
          filters:
          - type: value
            key: status.restrictedServices[]
            value: spanner.googleapis.com
            op: in
            value_type: swap
          actions:
            - type: notify
              to:
                - email@address
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/vpc
