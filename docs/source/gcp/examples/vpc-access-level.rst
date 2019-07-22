VPC Access levels - Set regions for an access level
====================================================

The following example shows how to set regions for a specific access level.

.. code-block:: yaml

    policies:
      - name: gcp-vpc-access-levels-patch
        resource: gcp.vpc-access-level
        query:
          - organization_id: 926683928810
        filters:
          - type: value
            key: title
            op: eq
            value: custodian_admin
        actions:
          - type: set
            description: new description
            basic:
                conditions:
                  - regions:
                    - BY
                    - US
                    - RU
