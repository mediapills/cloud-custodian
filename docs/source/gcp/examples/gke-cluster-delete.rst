GKE - Delete Clusters
=====================

Data governance strategy of an organization may allow only certain regions to be used for running 
GKE clusters and related resources.

The following policy automatically deletes all GKE clusters that are not located in the white 
list of regions.

Please note that when you delete an existing GKE cluster, most of its resources are deleted 
as well. Refer to GCP documentation for more details.

.. code-block:: yaml

    policies:
      - name: gke-cluster-delete-other-locations
        resource: gcp.gke-cluster
        filters:
          - type: value
            key: locations
            op: not-in
            value: [asia-east1-a, asia-east1-b, asia-northeast1-a]
        actions:
          - type: delete
