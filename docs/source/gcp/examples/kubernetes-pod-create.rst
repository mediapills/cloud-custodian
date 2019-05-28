Kubernetes - Example 1
=======================

The example shows how to notify to Cloud Pub/Sub information about {details} ....

Details about all available kubernetes resources are available at the :ref:`gcp_kubernetes` page.

To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies users if the GKE CreatePod action appears in the logs.

.. code-block:: yaml

    policies:
        - name:
          description: |
            Kubernetes. List of clusters node pools
          resource: gcp.gke-cluster-nodepool
          mode:
            type: gcp-audit
            methods:
            - "io.k8s.core.v1.pods.create"
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kubernetes
