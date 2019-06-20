Kubernetes - Control Node Pools Settings
=======================

Node pools are a set of nodes (i.e. VM's), with a common configuration and specification, under the control of the cluster master. NodePool resource contains the name and configuration for a cluster's node pool. Custodian can chech that all pool configurations follow established convention and/or devops best practices.

The example shows how to notify to Cloud Pub/Sub information about {details} ....

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy notifies if

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
