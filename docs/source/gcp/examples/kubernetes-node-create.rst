Kubernetes - Control Cluster Settings
=======================

In GKE, a cluster consists of at least one master and multiple worker machines called nodes. A cluster is the foundation of GKE: the Kubernetes objects that represent your containerized applications all run on top of a cluster. Custodian can check that configurations of all clusters in your organization follow an established devops convention and/or best practices.

Note that the ``notify`` action requires a Pub/Sub topic to be configured. To configure Cloud Pub/Sub messaging please take a look at the :ref:`gcp_genericgcpactions` page.

In the example below, the policy reports clusters which maintenance window (its start time) differs from a recommended value (e.g., 03:00 GMT).

.. code-block:: yaml

    policies:
      - name: gke-policy
        description: |
          Kubernetes. List of clusters
        resource: gcp.gke-cluster
        mode:
        filters:
         -  type: value
            key: maintenancePolicy.window.dailyMaintenanceWindow.startTime
            op: not-equal
            value: "03:00"
        actions:
          - type: notify
            subject: non-standard k8s clusters
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kubernetes
