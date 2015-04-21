.. _appendix:

==========================================
Appendix A - Generating html documentation
==========================================

This appendix covers how to generate html files from the ReStructured text documentation source files.  The documentation is generated using the Sphinx documentation tool.   Sphinx is a tool that makes it easy to create intelligent and beautiful documentation.

Generating the documentation is very easy.  First you need to download and install Sphinx if you don't already have it.  Then you use the command line to run the sphinx build tool, which will generate the documentation in the target format.

There are two ways of generating the documentation.  You can either use the supplied Makefile in the resources directory or you can use 'sphinx-build' directly.  The Makefile is setup to use specific locations, but these location can be overridden when invoking the make command.  The 'sphinx-build' application requires the source directory, the build directory, the configuration directory and the documentation target format to be supplied on the command line.

The commands for these two methods of generating the documentation are given here::

  # Method 1.
  make -f docs/resources/Sphinx.Makefile html
  
  # Method 2.
  sphinx-build -t html docs build

note:

 - This assumes your current working directory is the parent of the 'docs' directory
 - If a directory 'build' doesn't exist in the current directory it will be created

That's it!  Now you can use your favourite webbrowser to read the documentation.  The 'index.html' file for method 1. is located in 'build/html' and for method 2. it is available in 'build'.