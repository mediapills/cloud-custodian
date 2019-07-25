VPC Service Controls - Update Access Levels
================================================

An AccessLevel is a label that can be applied to requests to GCP services, along with a list of requirements necessary for the label to be applied. BasicLevel is an AccessLevel using a set of recommended features and it is composed of Conditions which are necessary for an AccessLevel to be granted. The Condition is an AND over its fields. 

The following policy sets new description for all AccessLevels that match the filter and also update their BasicLevel with a chosen set of regions.

.. code-block:: yaml

    policies:
      - name: gcp-vpc-access-levels-patch
        resource: gcp.vpc-access-level
        query:
          - organization_id: 926683928810
        filters:
          - type: value
            key: title
            op: regex
            value: ^(production?)\w+
        actions:
          - type: set
            description: updated by Custodian
            basic:
                conditions:
                  - regions:
                    - BY
                    - US
                    - JP
