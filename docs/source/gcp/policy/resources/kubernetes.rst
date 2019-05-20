.. _gcp_kubernetes:

Kubernetes
===========

Filters
--------
 - Standard Value Filter (see :ref:`filters`)

Actions
--------
 - GCP Actions (see :ref:`gcp_genericgcpactions`)

Environment variables
---------------------
To check the policies please make sure that following environment variables are set:

- GOOGLE_CLOUD_PROJECT

- GOOGLE_APPLICATION_CREDENTIALS

The details about the variables are available in the `GCP documentation to configure credentials for service accounts. <https://cloud.google.com/docs/authentication/getting-started>`_

Example Policies
----------------

Kubernetes. Clusters
~~~~~~~~~~~~~~~~~~~~~
The resource works with `cluster <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name:
          description: |
            Kubernetes. List of clusters
          resource: gcp.gke-cluster
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kubernetes

Kubernetes. Clusters node pools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The resource works with `clusters node pools <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name:
          description: |
            Kubernetes. List of clusters node pools
          resource: gcp.gke-cluster-nodepool
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kubernetes

Kubernetes. Operations
~~~~~~~~~~~~~~~~~~~~~~~
The resource works with `operation <https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.operations>`_ GCP REST resource. Fields that are provided by the REST resource can be used in the policy filter.

.. code-block:: yaml

    policies:
        - name:
          description: |
            Kubernetes. List of operations
          resource: gcp.gke-operation
          actions:
            - type: notify
              to:
                - email@email
              format: json
              transport:
                type: pubsub
                topic: projects/cloud-custodian/topics/kubernetes
