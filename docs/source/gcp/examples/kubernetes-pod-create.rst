Kubernetes - Control Settings of Node Pools
=======================

Node pools are a set of nodes (i.e. VM's), with a common configuration and specification, under the control of the cluster master. NodePool resource contains the name and configuration for a cluster's node pool. Custodian can check that all pool configurations follow an established devops convention and/or best practices.

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy reports pools where auto-upgrade option is switched off and therefore their nodes may be not up to date with the latest release version of Kubernetes.

.. code-block:: yaml

    policies:
        - name:
          description: |
            Kubernetes. List of clusters node pools
          resource: gcp.gke-cluster-nodepool
          filters:
            - type: value
              key: management.autoUpgrade
              op: not-equal
              value: true
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kubernetes
