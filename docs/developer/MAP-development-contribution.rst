.. _Developer Contribution for MAP Client:

=================
Contributing Code
=================

This section describes how a developer can contribute code to the MAP Client project.  Before reading this section make sure you have read through :doc:`Setup <MAP-development-setup>` as some of what follows may not make sense without this prior context.

.. contents:

Overview
========

To contribute code to the MAP Client project you should select an issue from the list of open issues to work on.  You can let others know that you are working on an issue by leaving a comment on the issue to that effect.  Once you have started work on the issue and added either some implementation, tests or documentation open a pull request to share your progress with other developers.

Add a reference from the main pull request to the src, tests and docs pull requests for a reviewer to follow.

Make use of Buildbot to test your changes, any changes (i.e. new commits) to an open pull request on MusculoskeletalAtlasProject/mapclient will trigger the test procedure.  Buildbot will report back to the pull request the status of the tests.  A reviewer will first look at the status of the main pull request before looking at anything else so having the tests pass is a priority.

When the changes you have completed resolves the issue a reviewer will give your work a final review before merging into the **prime** codebase. 

Fixing a bug follows a similar path the only difference being that we need to write a test that triggers the bug in question.

Finally check out :doc:`Git Submodules <MAP-development-submodules>` for help on working with git submodules. 

Take Ownership
==============

Because every feature must have an associated issue leave a comment on the issue letting others know that you are intending to start work on this issue.  If an issue has not been created for the functionality that you require simply create a new one and leave a comment stating that you are working on it.

Share Progress
==============

We are following a test driven approach for the MAP Client project so the first thing to do is write a test that at least covers some part of the functionality required for the feature you are working on.  Once this first test is written commit your changes and push them to Github so that your work can be shared with others.

When the first new test is pushed to Github create a pull request from your feature/develop branch against the MusculoskeletalAtlasProject/mapclient repositories develop branch.  We do this so that other developers can comment and make suggestions on your changes.  We want to have an environment of friendly social coding where developers can offer guidance and help minimise wasted effort.  Link this pull request to the main pull request by adding a comment on the main pull request with the following markup::

    MusculoskeletalAtlasProject/mapclient-tests#4
    
or::
 
    MusculoskeletalAtlasProject/mapclient-tests/pull/4

Github will interpret this markup and create a link between the pull requests.  Obviously replace the numeral '4' with the actual value of the related pull request for your own work.

With the tests written and any comments from the community resolved write the implementation code, the implementation code is written into your copy of the mapclient-src repository.  Again commit your code and push the changes to Github.  With the new code on Github create another pull request from your repository to the develop branch in the MusculoskeletalAtlasProject/mapclient-src repository.  Link this pull request to the main pull request again by adding a comment on the main pull request with the following markup::

    MusculoskeletalAtlasProject/mapclient-src#4
    
or::
 
    MusculoskeletalAtlasProject/mapclient-src/pull/4

Again, obviously replace the numeral '4' with the actual value of the related pull request for your own work.

Simarlarly to writing the implementation code you also need to write documentation for your changes and create a pull request from your mapclient-docs repository to MusculoskeletalAtlasProject/mapclient-docs develop branch.  Also link the pull request to the pull request already added for the tests by adding a comment on the main pull request with the following markup::

    MusculoskeletalAtlasProject/mapclient-docs#4
    
or::
 
    MusculoskeletalAtlasProject/mapclient-docs/pull/4

Again, replace the numeral '4' with the actual value of the related pull request for your own work.

To have your progress tested push a commit to the main pull request with the correct submodule references set making sure that the dependent pull requests (tests, src, docs) have the commits you are referencing.  When the commit is received by Github Buildbot will be notified and check for any changes, clone and run the tests across the Buildslaves.  When the tests have completed the status will be reported back to the main pull request and the commit status will be made visible on Github.

Final Review
============

When you have finished working on an issue, mark it as closed.  This will indicate to a reviewer that your work is ready for merging.  A reviewer will give your work a final review and when any queries are satisfactorily resolved they will merge and close the three open pull requests across mapclient-{tests, src, docs} and then close the main pull request.  All that is left to do now is to thank you for your contribution.

Thank you.

