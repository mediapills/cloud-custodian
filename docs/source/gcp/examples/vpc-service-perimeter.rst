VPC Service Controls - Restore Defaults for an Access Level of Perimeters
==============================================================================

With VPC Service Controls, you can configure security perimeters around the resources of your Google-managed services and control the movement of data across the perimeter boundary. 

An AccessLevel is a label that can be applied to requests to GCP services, along with a list of requirements necessary for the label to be applied. BasicLevel is an AccessLevel using a set of recommended features and it is composed of Conditions which are necessary for an AccessLevel to be granted. The Condition is an AND over its fields. 

The status has an information about resources, access levels, restricted services.

The example shows how to set a description and a status for service perimeters with specific access level.

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
