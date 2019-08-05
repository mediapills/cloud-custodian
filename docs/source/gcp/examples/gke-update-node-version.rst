GKE - Enforce Kubernetes Version in Use
=======================================

An essential security task is to control versions and enforce new updates, so known
vulnerabilities and holes are timely closed.

In the example below, all GKE clusters with node version equal to "1.12.8-gke.10" will be updated
to "1.13.6-gke.13".

Please note that a cluster's master and nodes are upgraded separately, also that downgrading a
cluster is not recommended in GCP documentation.

.. code-block:: yaml

    policies:
      - name: gke-cluster-update-node-version
        resource: gcp.gke-cluster
        filters:
          - type: value
            key: currentNodeVersion
            value: 1.12.8-gke.10
        actions:
          - type: update
            nodeversion: 1.13.6-gke.13
