.. _MAP-plugin-authoring:

====================
MAP Plugin Authoring
====================

The plugin lies at the heart of the MAP framework and the Plugin Creator Wizard creates skeleton plugins conforming to the MAP framework plugin interface.  The Plugin Creator Wizard assists with the initial plugin creation allowing the plugin developer to concentrate on implementing the plugins task.  For basic familiararity with the MAP Client please read the feature demonstration document :doc:`MAP-feature-demonstration`.

For more detailed information on the plugin interface read the :doc:`MAP-plugin` document, this document defines the plugin interface that the new plugin must adhere to.

Provenence Tracking
===================

The steps for adding a skeleton plugin to a git repository is

   #. Create a repository on GitHub, add Python based .gitignores file
   #. cd into teh directory where skeleton plugin was created
   #. Link the repository and make the first commit with the following commands::
   
      git init .
      git remote add origin <repository location from above>
      git pull -u origin master
      git add .
      git commit -m "Initial commit of skeleton step."
      git push -u origin master
      
   #. [Optional] If using eclipse add the following lines to the .gitignore file::
   
      # Eclipse PyDev
      .project
      .pydevproject

