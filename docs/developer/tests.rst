Testing
=======
Several unit tests are present in the ``psipy/*/tests`` directories. These
are written to protect against code being unintentionally changed such that
either the code itself raises an error or what the code returns is unexpected.

Local testing
-------------
To install the packages required for running the tests, change to the root
directory of the psipy source code and run::

  pip install .[tests]

To run the tests, stay in the same directory and run::

  pytest

Most of the tests require data files. HDF4 files are automatically downloaded,
but MAS HDF5 and PLUTO files have to be manually added. These should be located in a user-created
folder within the source directory called :file:`data`, which itself should
contain the following test file directories:

- :file:`mas_hdf4`: the files from a MAS output in HDF4 format
- :file:`mas_hdf5`: the files from a MAS output in HDF5 format
- :file:`pluto`: the files from a PLUTO output

Continuous integration
----------------------
Every time a new commit is pushed to the 'main' branch on github, github actions
runs the tests automatically. The most recent runs can be seen at
https://github.com/predsci/PsiPy/actions

Code coverage
-------------
The coverage (ie. which lines are/aren't covered
by the tests) is also automatically reported by codecov, and can be seen at
https://codecov.io/gh/predsci/PsiPy.
