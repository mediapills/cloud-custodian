Key Management System - Audit Crypto Key Version destruction
============================================================

Custodian can audit and notify if a Version for a KMS Cryptographic Key has been destroyed.

Details about all available Key Management System resources are available at the :ref:`gcp_kms` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

.. code-block:: yaml

    policies:
        - name: gcp-kms-cryptokey-version-audit-destruction
          resource: gcp.kms-cryptokey-version
          mode:
            type: gcp-audit
            methods:
              - DestroyCryptoKeyVersion
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/dns