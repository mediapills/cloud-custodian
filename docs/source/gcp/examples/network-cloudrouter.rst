Network - Check if there are unattached Cloud Routers
============================================================
Custodian can check and delete unused Cloud Routers (those that don't have any attached interface like VPN tunnel etc.)

In the example below, the policy finds and deletes unused routers.

.. code-block:: yaml

    policies:
      - name: gcp-network-unattached-routers
        description: Checks unattached Cloud Routers
        resource: gcp.router
        filters:
           - type: value
             key: interfaces
             value: absent
        actions:
           - delete