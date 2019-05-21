Key Management System - Audit Crypto Key creation
=================================================

Custodian can audit and notify if a KMS Cryptographic Key has been created.

Details about all available Key Management System resources are available at the :ref:`gcp_kms` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-kms-cryptokey-audit-creation
          resource: gcp.kms-cryptokey
          mode:
            type: gcp-audit
            methods:
              - CreateCryptoKey
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dns