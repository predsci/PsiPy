Reading HDF files directly
===========================

Although PsiPy provides higher-level routines for reading all the data from a
MAS run into your Python environment, we also provide some lower-level routines
in case you just want to see the data, or do not want all the added features 
that come with these routines. 

So, to read a MAS vr, say, HDF file into a NumPy array, type: 

.. code-block:: python

  filename = "/path-to-files/vr002.hdf"
  r,theta,phi,vr=rdhdf_3d(filename)

where r, theta, and phi are the usual sppherical coordinates giving the 
locations of the grid points, and, in this case, vr is the variable being 
read in.

At this point, you can treat r,theta,phi, and vr as you would any other 
NumPy arrays. 

For example, to convert from colatitude to latitude, radians, to degrees, and 
to plot a slice of the variable as a function of longitude and latitude, you 
can run the following commands:

.. code-block:: python

  ir = 100
  lat_deg = (pi/2. - theta)*rad2deg
  lon_deg = phi*rad2deg
  p1 = contourf(lon_deg,lat_deg,transpose(vr[:,:,ir]), xtitle="Longitude (Deg)", \
  ytitle="Latitude (Deg)", levels=50, xticks=[0,90,180,270,360], \
  yticks=[-90,-60,-30,0,30,60,90],colorbar=1)

Note that this relies on 'contourf', a python function that will be included 
in the near future (and also relies on 'rad2deg', which is what it says :) )

In addition to 'rdhdf_3d', you can also call 'rdhdf_2d' and 'rdhdf_1d', which,
as their name suggests, read MAS 2D and 1D HDF files. 

For example:

.. code-block:: python

  theta,phi,vr=rdhdf_2d(filename)
  r,var=rdhdf_1d(filename)

Finally, if you read in MAS data, manipulate it, and want to write the
resulting array out as a MAS HDF routine, you can use the wrhdf function: 

.. code-block:: python

   wrhdf_3d(hdf_filename,x,y,x,f)
   wrhdf_2d(hdf_filename,x,y,f)
   wrhdf_1d(hdf_filename,x,f)

Bear in mind that while these routines do as advertised, they are cannot be
combined with the added features of the high-level functions. Note also that
when you read the data in using this simpler approach, the variables remain in
code units. You will need to multiple them by the appropriate factor to
generate values in cgs or MKS. 
