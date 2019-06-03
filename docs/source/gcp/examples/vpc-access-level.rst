VPC - Access levels in a region
================================

It described below how to notify to Cloud Pub\Sub information about available access levels in BY region.

Details about all available VPC resources are available at the :ref:`gcp_vpc` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: access-level-for-by-region
          description: |
            VPC. List of Service Perimeters
          resource: gcp.vpc-access-level
          query:
            - organization_id: <organization_id>
          filters:
          - type: value
            key: basic.conditions[].regions[]
            value: BY
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
