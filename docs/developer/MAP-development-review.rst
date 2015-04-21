.. _Developer Review for MAP Client:

========================
Final Development Review
========================

This section describes how a reviewer reviews a tranche of work for inclusion in the MusculoskeletalAtlasProject/mapclient-{tests,src,docs} repositories.

Overview
========

The job of the reviewer is to make sure any submitted code meets the standard required for the project.  The things to take particular notice of are:

* Have appropriate tests been written
* Is the coding standard followed
* Is the documentation satisfactory
* Are the SHA values in the pull requests the ones that were tested
* Are the pull requests against the develop branch

If you are satisfied with the code in the pull requests, merge and close each open pull request except the pull request to MusculoskeletalAtlasProject/mapclient and then use Buildbot to synchronise the meta repository MusculoskeletalAtlasProject/mapclient.

Final Review
============

The final review stage is the last opportunity for changes before inclusion into the **prime** repositories so it is important to make sure proper tests have been written and that the coding standard has been followed.  The documentation must be accurate and complete it is often the first point of contact for new users and the better the documentation the better the project.

Another item to take careful note of is the SHA values in the pull requests match those that were actually tested by Buildbot.  Perhaps in the future there will be a script that will make this check for us but for now it is the responsibility of the reviewer.

When you are satisfied merge and close the three open pull requests attached to the submodule repositories and close the open pull request to MusculoskeletalAtlasProject/mapclient without merging.

Synchronise Submodules
======================

Go to the Buildbot homepage and choose the builders link at the top of the page.  Select the sync builder and authenticate yourself with Buildbot.  Fill in the required values and force the build.  The synchronisation script will not run as intended if the pull requests referenced have not been merged and closed beforehand.

