Key Management System - Set state Crypto Key Version
====================================================

In the example below, the policy allow to destroy Hardware Security Module (HSM).

.. code-block:: yaml

    policies:
      - name: gcp-kms-cryptokey-version-set
        resource: gcp.kms-cryptokey-version
        filters:
          - type: value
            key: protectionLevel
            op: in
            value: [SOFTWARE, HSM]
        actions:
          - type: set
            state: ENABLED
