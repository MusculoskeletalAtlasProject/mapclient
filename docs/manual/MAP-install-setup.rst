.. _MAP-install-setup:

=======================================
MAP Client Installation and Setup Guide
=======================================

This document describes how to install and setup the MAP Client software for use on your machine.
The MAP Client software is a Python application that uses the PySide6 Qt library bindings.

The `Installation`_ section details getting the MAP Client and it's dependencies installed on your system.
There are two main ways of getting the MAP Client installed on your operating system.  This document will cover both of those methods.

For people who are only running existing workflows the suggested installation method is `Install Using Pre-Built Binary`_.
For plugin developers the suggested method is to `Install Using Pip`_.

The `Install Using Pre-Built Binary`_ method is covered first followed by the instructions on how to `Install Using Pip`_.
For most operating systems Python is already installed, but for some, most notably Windows based operating systems, it is not.
For instructions on installing Python for Windows based operating systems see the `Installing Python on Windows`_ section.

The `Setup`_ section details getting the MAP Client setup with external plugins.

------------
Installation
------------

Install Using Pre-Built Binary
------------------------------

For Windows there is an installer application available from:

  https://github.com/MusculoskeletalAtlasProject/mapclient/releases/

Download and install the package.


Install Using Pip
-----------------

Pip is a tool for installing and managing Python packages.
It is particularly suited for the installation and management of source distributions of Python software, of which the MAP Client is one.

From the command line we can install MAP Client with the following command::

  pip install mapclient

The MAP Client application should now be installed on your system.  It can be launched from the command line with this command::

  mapclient

which should result in an application window similar to that shown below.

.. figure:: images/map_client_barebones.png
   :align: center
   :width: 80%

The MAP Client relies heavily on plugins to do anything interesting, you can either create these yourself or add already available ones to your application by downloading them and using the Plugin Manager Tool in the MAP Client, read the documents :ref:`MAP-feature-demonstration` and :ref:`MAP-plugin-wizard` to learn more.

Install Using Git
-----------------

Git is a distributed revision control tool.
GitHub utilizes Git for open source project hosting, this is where the MAP Client source code is situated.
To get 'git', use your system's package management system to install it. If you are using windows you can download and install it from:

    http://git-scm.com/downloads/guis

Then, use *Git* to clone the MAP Client source code to your system::

    git clone https://github.com/MusculoskeletalAtlasProject/mapclient.git

Finally, run the MAP Client *setup* script to install it::

    pip install .

Note that the line above should be run from the same directory as the previous command.

Installing Pip
--------------

Pip is a tool for installing and managing Python packages.  It relies on setuptools to work.
First you must install setuptools, which has detailed instructions available here

  https://pypi.python.org/pypi/setuptools#installation-instructions

Next, to make sure that easy_install is installed correctly, open a command window and issue the command::

  easy_install --version

If this command prints out the version of setuptools you have installed then you can install pip with the command::

  easy_install pip

otherwise you will probably need to adjust the PATH system variable so that the easy_install application is available. 

Installing Python on Windows
----------------------------

This section is for setting up Python on Windows as other operating systems supported by the MAP Client already have Python installed.
The MAP Client framework is written in :term:`Python` and is designed to work with Python 3.
The MAP Client framework is tested against Python 3.7, 3.8 and 3.9 and should work with any of these Python libraries.

The current recommendation is to choose the 64 bit version of the latest Python 3.9 binary release.
Current versions of Python are available from:

    http://www.python.org/download/

Download an MSI installer that matches your choices and follow the onscreen prompts.  We recommend adding the ``Python`` and ``Python\Scripts`` folders to your system ``PATH``.

-----
Setup
-----

External Plugins
----------------

.. _github orginisation: https://github.com/mapclient-plugins

The installation of external MAP Client plugins is a two step process.
The first step is to download the plugins onto the local file system, the second step is to use the :ref:`MAP plugin manager <MAP-plugin-manager-tool>` tool to identify the plugins and load them into the MAP Client.

There is a `github orginisation`_ which has a collection of MAP Client plugins.
