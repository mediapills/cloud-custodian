VPC Service Controls - Enforce Configuration of Service Perimeters
==================================================================

With VPC Service Controls, you can configure security perimeters around the resources of your Google-managed services via describing a set of GCP resources which can freely import and export data amongst themselves, but not export outside of the perimeter boundary.

The policy below replaces any existing configuration of the target perimeter with two chosen `AccessLevel` sets applicable to BigQuery and Cloud PubSub services in the specified GCP projects within an organization.

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
            description: updated by Custodian
            status:
              resources:
                - projects/359546646409
                - projects/2030697917
              accessLevels:
                - accessPolicies/1016634752304/accessLevels/custodian_viewer_new
                - accessPolicies/1016634752304/accessLevels/custodian_viewer_new2
              restrictedServices:
                - bigquery.googleapis.com
                - pubsub.googleapis.com
