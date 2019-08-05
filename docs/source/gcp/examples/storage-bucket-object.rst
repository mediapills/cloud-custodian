Storage - Watch Sensitive Objects for Changes
=============================================

Objects are pieces of data that are uploaded to Google Cloud Storage. Custodian can audit metadata of objects including their ACLs and report any suspicious activity - e.g., if 'update' or 'patch' operations were performed either via GCP Concole, API or shell.

In the example below, the policy set action was performed on objects of ColdLine storage class for update storageClass.

.. code-block:: yaml

    policies:
      - name: gcp-bucket-object-update
        resource: gcp.bucket-object
        mode:
          type: gcp-audit
          methods:
            - storage.objects.update
        filters:
          - type: value
            key: storageClass
            value: STANDARD
        actions:
          - type: set
            class: MULTI_REGIONAL
