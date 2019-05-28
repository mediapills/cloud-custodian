Kubernetes - Example 2
=======================

The example shows how to notify to Cloud Pub/Sub information about {details} ....

Details about all available kubernetes resources are available at the :ref:`gcp_kubernetes` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies users if the GKE CreateNode action appears in the logs.

.. code-block:: yaml

    policies:
      - name: gke-policy
        description: |
          Kubernetes. List of clusters
        resource: gcp.gke-cluster
        mode:
          type: gcp-audit
          methods:
          - "io.k8s.core.v1.nodes.create"
        actions:
          - type: notify
            subject: k8s cluster has been created
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kubernetes
