Testing
=======

To install the packages required for running the tests, change to the root
directory of the psipy source code and run::

  pip install .[tests]

To run the tests, stay in the same directory and run::

  pytest

Most of the tests require data files. These should be located in a user-created
folder within the source directory called :file:`data`, which itself should
contain the following test file directories:

- :file:`mas_hdf4`: the files from a MAS output in HDF4 format
- :file:`mas_hdf5`: the files from a MAS output in HDF5 format
- :file:`pluto`: the files from a PLUTO output
