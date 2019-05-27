.. _gcp_network:

Network
===========

Filters
--------
 - Standard Value Filter (see :ref:`filters`)
    Fields for filtering can be received from GCP resource object. Link to appropriate resource is
    provided in each GCP resource.

Actions
--------
 - GCP Actions (see :ref:`gcp_genericgcpactions`)

Example Policies
----------------

Network. Cloud Routers
~~~~~~~~~~~~~~~~~~~~~~
`GCP resource: Cloud Routers <https://cloud.google.com/compute/docs/reference/rest/v1/routers/list>`_

.. code-block:: yaml

    policies:
      - name: gcp-network-unattached-routers
        description: Network. List of Cloud Routers
        resource: gcp.router
        actions:
           - type: notify
             to:
               - email@address
             format: txt
             transport:
               type: pubsub
               topic: projects/my-gcp-project/topics/my-topic
