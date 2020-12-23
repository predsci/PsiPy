Installing
==========

Requirements
------------
psipy requires python >= 3.7 . To load hdf4 files you will need a working
installation of the `HDF4 library`_. If you are using the conda environment
manager this can be installed with:

.. code-block:: bash

  conda install hdf4

On ubuntu this can be installed with:

.. code-block:: bash

  apt install libhdf4-dev

.. _HDF4 library: https://portal.hdfgroup.org/display/support/Download+HDF4

Installing psipy
----------------
Currently the only way to install psipy is from source. Change to the directory
you want to download the source too, and run:

.. code-block:: bash

  git clone https://github.com/predsci/PsiPy
  cd PsiPy
  pip install .

This will automatically install psipy and it's dependencies.
