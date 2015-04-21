.. Developer Documentation for MAP Client

==================================
MAP Client Developer Documentation
==================================

This section of documentation is intended for developers.  It covers a range of topics from getting setup through to how code reviews are done.  MAP Client uses Git for source code management (SCM), Buildbot for continuous integration testing and Github to host the software on the web.  The way in which these elements are brought together and how a developer is expected to use them forms the development process which is defined here.

The repository at https://github.com/MusculoskeletalAtlasProject/mapclient is the definitive repository for the software and used for creating software releases.  We will refer to this repository as the **prime** repository.  The developer documentation describes the Git branching model in use on the **prime** repository and the process to follow for getting new code added to this repository.  The **prime** repository makes use of Git submodules to enable modularisation of the codebase for use in other environments.  Using Git submodules creates a divergence from the standard way people are currently using Github.  For this reason it is recommended that you read this documentation to understand how to develop code for the MAP Client project.  The process is designed to be as standard as possible with modifications to handle the awkwardness imposed by using submodules.  We also make use of Buildbot to automate some of the process to make development easier for new developers and reviewers.

Contents:

.. toctree::
   :maxdepth: 2
   :titlesonly:

   MAP-development-setup
   MAP-development-gitbranching
   MAP-development-contribution
   MAP-development-review
   MAP-development-codingstandard
   MAP-development-release
   MAP-development-submodules
   MAP-development-buildbotaccess
   
   appendix