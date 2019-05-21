Key Management System - Audit Crypto Key protection level
=========================================================
Custodian can audit and notify if a KMS Cryptographic Key has been created using the wrong settings. Note that the ``notify`` action requires a Pub/Sub topic to be configured.

In the example below, the policy is set to filter Keys with protection level other than Hardware Security Module (HSM).

.. code-block:: yaml

    policies:
        - name: gcp-kms-cryptokey-audit-creation
          resource: gcp.kms-cryptokey
          mode:
            type: gcp-audit
            methods:
              - CreateCryptoKey
          filters:
            - type: value
              key: primary.protectionLevel
              op: not-in
              value:
                - HSM
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/my-gcp-project/topics/my-topic
