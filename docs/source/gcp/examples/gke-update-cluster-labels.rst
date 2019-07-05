GKE - Label Clusters Depending on Their Properties
===================================================

You may want to organize your existing GKE clusters with labels as a pre-requisite to use other scripts and policies and/or in order to create a better traceability of clusters in GCP console.

In the example below, the policy marks clusters of 3 nodes with "nodes:minimal" label.

.. code-block:: yaml

    policies:
      - name: gke-cluster-set-label
        resource: gcp.gke-cluster
        filters:
          - type: value
            key: currentNodeCount
            value: 3
        actions:
          - type: set
            labels:
                - key: nodes
                  value: minimal
