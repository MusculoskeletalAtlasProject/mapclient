MAP Client Documentation
========================

The documentation for MAP Client is written for Sphinx in reStructuredText.  It is easiest to read the documentation in
a Sphinx processed form. Refer to the Sphinx documentation for the details on turning reStructuredText into a processed
form that best suits your requirements. Information on installing Sphinx is available `here <https://www.sphinx-doc.org/en/master/usage/installation.html>`__ and the quick start
instructions are available `here <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`__

A processed form of the documentation is available from `readthedocs <https://map-client.readthedocs.io/>`_.  The reStructuredText files
in the repository are for making additions or changes and not general consumption.

Should the user desire to make any changes to the documentation, it is relatively easy to re-generate the html files from
the reStructuredText documentation using Sphinx. This process is described as follows. On the command line, set the current
directory to the location of the :code:`docs` directory on the user's drive (here we assume that you have the MAP Client source code available in the directory :code:`mapclient`)::

    cd <Local Directory>\mapclient\docs

Then, run the following command::

    make html

The updated html files can then be found in :code:`<Local Directory>\mapclient\docs\_build\html`. :code:`index.html` is the entry to the documentation.
View the documentation by directing your web browser to :code:`<Local Directory>/mapclient/docs/_build/html/index.html`.

If the user encounters any issues with the make command: Windows users should be using cmd.exe rather than any command line
alternatives; macOS and Linux users should ensure that (GNU) make is installed. Otherwise, the problem is likely to be related
to the installation of Sphinx.
