.. _Developer Git submodules for MAP Client:

==============
Git Submodules
==============

This section offers help on working with Git submodules as used by the MAP Client project.

.. contents::

Overview
========

It is recommended to use a prompt assistance when dealing with Git from the command line so that you will not lose track of which branch you are currently working on.  Also make use of the Git submodule command foreach option to perform the same operation across all submodules.


Branching
=========

.. code::

  git submodule foreach git checkout -b mybranch
  git checkout -b mybranch


