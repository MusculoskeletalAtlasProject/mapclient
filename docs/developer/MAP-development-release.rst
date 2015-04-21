.. _Development Release for MAP Client:

==================
Managing a Release
==================

This document describes the process for managing a release for MAP Client.

.. contents::

Overview
========

The process of creating a release is a five stage process, three of these stages are managed through Buildbot the other two are managed by the developer.  Only authorised users can start the release process.  The five stages of the release process are:

#. Prepare release
#. Test release and fix any minor bugs
#. Create release
#. Unprepare release for merging any bugfixes back into develop branch (may not be required if no bug fixes were made)
#. Delete release branch

Buildbot will manage stages 1, 3, and 5.  In stage 4 you can use the unprepare script to undo changes made by Buildbot in the first stage.

Prepare Release
===============

To prepare for a release use Buildbot to create a branch for the upcoming release through the 'prepare' builder.  To create the release branch complete the following tasks:

#. Goto http://autotest.bioeng.auckland.ac.nz/mapclient-buildbot/builders/prepare
#. Login to Buildbot
#. Choose the branch where the release should be created from.  A release from the develop branch will create a 'release-*' branch.  A release from the master branch will create a 'hotfix-*' branch.
#. Set the version number for the release, this value will be appended to the branch name.
#. Click the 'Force Build' button

When the 'Force Build' button is clicked Buildbot will run a script to create a release branch.  The new branch will be branched from the current tip of the develop/master branch.  The version number will be set for the upcoming release and the changes will be commited and pushed to MusculoskeletalAtlasProject/mapclient on Github.

Test and Bug Fix
================

In this stage you should do a final check looking at the tests, source code, and documentation making sure nothing has slipped through the review process.  If any minor issues arise fix them and merge them into the release branch through a merge request.  If a major issue becomes apparent abandon the release by moving onto stage 5 directly. 
  
Create Release
==============

To create a release use Buildbot to merge a specified release branch into master and tag the commit set with the version number.  To create a release complete the following tasks:

#. Goto http://autotest.bioeng.auckland.ac.nz/mapclient-buildbot/builders/release
#. Login to Buildbot
#. Set the name of the branch where the release is to be made from, for example 'release-0.1.0'
#. Click the 'Force Build' button

When the 'Force Build' button is clicked Buildbot will run a script to create a release.  The release branch will be merged into master and the commit set will be tagged with the version number obtained from the branch name. 

Unprepare Release
=================

After the release has been created you will need to semi-manually unprepare the release.  This stage is only required if changes were merged into the release branch in stage 2.  If changes have been merged then you will need to run the unprepare script to undo changes made in stage 1 and then merge the remaining changes back into develop.  Merging back into develop from the release branch is a manual task as it often involves conflicts which require resolving before the merge can take place.

Delete Release
==============

At this point the release branch has served it's purpose and is no longer needed.  To delete the release branch complete the following tasks:

#. Goto http://autotest.bioeng.auckland.ac.nz/mapclient-buildbot/builders/delete
#. Login to Buildbot
#. Set the name of the branch which is to be deleted, for example 'release-0.1.0'
#. Click the 'Force Build' button



