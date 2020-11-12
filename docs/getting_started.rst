Getting started
===============

psipy is a package for loading and visualising the output of PSI's MAS model
runs. This page provides some narrative documentation that should get you up
and running with obtaining, loading, and visualising some model results.

Getting data
------------
The PSI MHDWeb pages give access to MAS model runs. The runs are indexed by
Carrington rotation, and for each Carrington rotation there are generally a
number of different runs, varying in the model used in the simulation and/or
the boundary conditions.

To load data with `psipy` you need to manually download the files you are
interested in to a directory on your computer. In this example we'll use the...

Loading data
------------
psipy stores the output variables from a single MAS run in the
`psipy.model.MASOutput` object. To create one of these, specify the directory
which has all of the outputs ``.hdf`` files you want to load::

    from psipy.model import MASOutput

    directory = '/path/to/files'
    mas_output = MASOutput(directory)

To see which variables have been loaded, we can look at the ``.variables``
attribute::

    print(mas_output.variables)
    # PUT OUTPUT HERE

This will print a list of the variables that have been loaded. Each individual
variable can then be accessed with e.g.::

    br = mas_output.br
    print(br)

Data coordinates
----------------
Each variable is stored in a `xarray.DataArray`. This contains the scalar
values of the data as a normal array, but in addition also stores the
coordinates of each data point. Full documentation for the `DataArray` object
can be found at PUT LINK HERE.

MAS model outputs are defined on a 3D grid of points on a spherical grid. The
coordinate names are ``'r', 'theta', 'phi'``.


Plotting data
-------------
