.. _MAP-main-index:

====================================================================
Musculoskeletal Atlas Project (MAP) Client Documentation - |version|
====================================================================

.. _MAP Client: https://simtk.org/home/map

The Musculoskeletal Atlas Project Client (`MAP Client`_) is a cross-platform framework for managing workflows.  A workflow consists of a number of connected workflow steps.  The MAP Client framework is a plugin-based application where the plugins are workflow steps.

The MAP Client framework has a number of tools for creating, managing and sharing workflows, workflow steps and the outputs generated from the workflow steps.  It is an application written in Python and based on Qt, the cross-platform application and UI framework.

One of the central ideas for the MAP Client is to allow users to easily develop and share their own plugins/workflow steps.  The requirements for developing a workflow step have been kept as low as practicable allowing creators to concentrate on the practical implementation of the workflow step rather than concerning themselves with conforming to the plugin API.  The Plugin Wizard tool greatly simplifies the first stage in creating a workflow step and generates a considerable amount of the skeleton code required.

Another of the central ideas for the MAP Client is making the output from the workflow steps available and searchable to others.  To achieve this the MAP Client uses the Physiome Model Repository (PMR).  PMR has been designed to provide data upload, storage and distribution capabilities, despite the name PMR is not just for models but for any data that users wish to track development changes of.  The MAP Client has the PMR Tool to make use of this facility.  Using the PMR Tool we can make sure the important data that a workflow produces is secure and available into the future.

A feature of having a plugin based framework is that it is possible for groups to share their workflows and workflow steps without requiring a lot of extraneous software.  Also having users create and share their plugins increases the flexibility of the MAP Client and distances users from relying on an external team of developers.  To further the reach of workflow steps if they are made to be as general as possible we can increase the re-usability and shareability for other users to use in their own work or alternatively extend to fit their purposes.

Further details on the MAP Client are available in the documents listed below.
 
.. toctree::
   :maxdepth: 1
   :titlesonly:
   
   manual/index
   developer/index
   
.. toctree::
   :hidden:
   
   README
   
   
Copyright
=========

This documentation is part of MAP Client.

MAP Client is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Copyright MAP Client Team Members