GKE - Enforce Standard Configuration of Node Pools
==================================================

A generally accepted devops practice is to standardize your infrastructure as much as possible 
and reasonable, so you can easily deploy new versions of your software or add a new component 
into infrastructure.

Node pools are a set of nodes (i.e. VM's), with a common configuration and specification, under 
the control of the cluster master. The policy below configures all node pools to be 
upgraded automatically and have the same initial size, as well as autoscaling constraints.

.. code-block:: yaml

    policies:
      - name: gke-cluster-nodepool-enforce-standard-configuration
        resource: gcp.gke-cluster-nodepool
        actions:
          - type: set-management
            auto-upgrade: 'true'
          - type: set-size
            node-count: '5'
          - type: set-autoscaling
            enabled: 'true'
            minNodeCount: '3'
            maxNodeCount: '10'
