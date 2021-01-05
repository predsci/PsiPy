Documentation
=============
The documentation is automatically generated from a combination of restructured
text files and code docstrings by sphinx and sphinx-gallery.

Narrative documentation
-----------------------
The narrative documentation (including this file!), and the overall structure
for the documentation is stored in :file:`psipy/docs`. The sub-directories
store the narrative documentation, and the docs directory stores the
configuration for building the documentation (:file:`conf.py`) and the index
file for the homepage (:file:`index.rst`).

API documentation
-----------------
The API is documented within individual documentation strings (docstring), that
live by the code itself in :file:`psipy/psipy`. The documentation for these is
then automatically generated in :file:`psipy/docs/api`.

Building locally
----------------
To install the requirements for building the docs locally, from the psipy
source directory run::

  pip install .[docs]

To build the docs locally, change to the :file:`docs` folder, and run::

  make html

Hosted builds
-------------
The documentation is automatically `built <https://readthedocs.org/projects/psipy/builds/>`__
and `hosted <https://psipy.readthedocs.io/en/latest/>`__ by readthedocs every
time a new commit is pushed to the 'main' branch on github.
