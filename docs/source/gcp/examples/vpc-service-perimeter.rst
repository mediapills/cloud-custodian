VPC Service perimeters - Restore default state for an access level
===================================================================

The example shows how to set a description and a status for service perimeters with specific access level.
The status has an information about resources, access levels, restricted services.

.. code-block:: yaml

    policies:
      - name: gcp-vpc-service-perimeters-patch
        resource: gcp.vpc-service-perimeter
        query:
          - organization_id: 926683928810
        filters:
          - type: value
            key: status.accessLevels
            op: contains
            value: accessPolicies/1016634752304/accessLevels/custodian_viewer
        actions:
          - type: set
            description: new description
            status:
                resources:
                  - projects/359546646409
                  - projects/2030697917
                accessLevels:
                  - accessPolicies/1016634752304/accessLevels/custodian_viewer
                  - accessPolicies/1016634752304/accessLevels/custodian_viewer_2
                restrictedServices:
                  - bigquery.googleapis.com
                  - pubsub.googleapis.com
