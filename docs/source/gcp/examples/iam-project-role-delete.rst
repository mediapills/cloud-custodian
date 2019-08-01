IAM - Delete Project Roles
==========================

To enforce security of your organization, Custodian can automatically delete any newly created custom project roles which are not included into a 'white list'.

The policy below deletes project roles which don't match the regexp.

.. code-block:: yaml

     policies:
       - name: gcp-iam-project-role
         resource: gcp.project-role
         filters:
           - type: value
             key: title
             op: regex
             value: ^(mycloud?)\w+
         actions:
           - type: delete
