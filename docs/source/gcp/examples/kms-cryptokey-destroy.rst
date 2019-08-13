Key Management System - Destroy Crypto Key Version
==================================================

In the example below, the policy allow destroy all cryptokey versions where protectionLevel 
does not equal SOFTWARE or HSM.

.. code-block:: yaml

    policies:
      - name: gcp-kms-cryptokey-version-destroy
        resource: gcp.kms-cryptokey-version
        filters:
          - type: value
            key: protectionLevel
            op: not-in
            value: [SOFTWARE, HSM]
        actions:
          - type: destroy
