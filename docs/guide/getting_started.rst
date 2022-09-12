Getting started
===============

psipy is a package for loading and visualising the output of PSI's MAS model
runs. This page provides some narrative documentation that should get you up
and running with obtaining, loading, and visualising some model results.

Getting data
------------
The PSI `MHDWeb pages`_ give access to MAS model runs. The runs are indexed by
Carrington rotation, and for each Carrington rotation there are generally a
number of different runs, varying in the type model run and/or
the boundary conditions.

To load data with psipy you need to manually download the files you are
interested in to a directory on your computer.

.. _MHDWeb pages: http://www.predsci.com/mhdweb/data_access.php

MAS and PLUTO data
------------------
psipy supports data from both MAS model runs and PLUTO model runs.
For simplicity the instructions in this guide are written with MAS model output in mind.
Everything works the same way for PLUTO model output though - just load the files with the `PLUTOOutput` class instead of the `MASOutput` class.
The one feature that is not yet implemented for PLUTO data is field line tracing.

Loading data
------------
psipy stores the output variables from a single MAS run in the `MASOutput`
object. To create one of these, specify the directory which has all of the
output ``.hdf`` files you want to load:

.. code-block:: python

    from psipy.model import MASOutput

    directory = '/path/to/files'
    mas_output = MASOutput(directory)

It is assmumed that the files have the filename structure
``'{var}{timestep}.hdf'``, where ``var`` is a variable name, and ``timestep``
is a three-digit zero-padded integer timestep.

To see which variables have been loaded, we can look at the ``.variables``
attribute:

.. code-block:: python

    print(mas_output.variables)

This will print a list of the variables that have been loaded. Each individual
variable can then be accessed with square brackets, for example to get the
radial magnetic field component:

.. code-block:: python

    br = mas_output['br']

This will return a `Variable` object, which stores the underlying data as a
`xarray.DataArray` under the `Variable.data` property.

Data coordinates
----------------
The data stored in `Variable.data` contains the values of the data as a normal
array, and in addition stores the coordinates of each data point.

MAS model outputs are defined on a 3D grid of points on a spherical grid. The
coordinate names are ``'r', 'theta', 'phi'``. The coordinate values along each
dimension can be accessed using the ``r_coords, theta_coords, phi_coords``
properties, e.g.:

.. code-block:: python

  rvals = br.r_coords

Sampling data
-------------
Variable objects have a `Variable.sample_at_coords` method, to take a sample of
the 3D data cube along a 1D trajectory. This is helpful for flying a 'virtual
spacecraft' through the model, in order to compare model results with in-situ
measurements.

`sample_at_coords` requires arrays of longitude, latitude, and radial distance.
Given these coordinates, it uses linear interpolation to extract the values
of the variable at each of the coordinate points.

For an example of how all this works, see :ref:`sphx_glr_auto_examples_sampling_plot_in_situ_comparison.py`.
