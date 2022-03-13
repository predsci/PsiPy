Visualization
=============

Matplotlib
----------
`Variable` objects have methods to plot 2D slices of the data. These
methods are:

- `Variable.plot_phi_cut`
- `Variable.plot_equatorial_cut`
- `Variable.plot_radial_cut`

A typical use looks like this:

.. code-block:: python

  ax = plt.subplot(1, 1, 1, projection='polar')
  model['rho'].plot_phi_cut(index, ax=ax, ...)

and produces an output like this:

.. image:: /auto_examples/visualisation/images/sphx_glr_plot_visualising_mas_002.png
   :width: 600

For more examples of how to use these methods, see the
:ref:`sphx_glr_auto_examples` gallery.

Animating timesteps
~~~~~~~~~~~~~~~~~~~
If multiple timesteps have been loaded, each of the above methods can either
be used to plot animations over time, or single time slices. By default they
will produce animations which then need to be manually saved. As an example,
to create and save an animated cut in the phi direction:

.. code-block:: python

  animation = model['rho'].plot_phi_cut(phi_index, ...)
  animation.save('my_animation.mp4')

Contouring data
~~~~~~~~~~~~~~~
There are also methods that can be used to plot contours of the data on top
of 2D slices. As an example, this can be helpful for plotting the heliospheric current sheet, by contouring :math:`B_{r} = 0`. These methods are

- `Variable.contour_phi_cut`
- `Variable.contour_equatorial_cut`
- `Variable.contour_radial_cut`

A typical use looks like this:

.. code-block:: python

  ax = plt.subplot(1, 1, 1, projection='polar')
  model['rho'].plot_phi_cut(index, ax=ax, ...)
  model['br'].contour_phi_cut(index, levels=[0], ax=ax, ...)

and produces outputs like this:

.. image:: /auto_examples/visualisation/images/sphx_glr_plot_visualising_mas_003.png
   :width: 600

For more examples of how to use these methods, see the
:ref:`sphx_glr_auto_examples` gallery.

Normalising data before plotting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sometimes it is helpful to multiply data by an expected radial falloff, e.g.
multiplying the density by :math:`r^{2}`. This can be done using the
`Variable.radial_normalized` method, e.g.:

.. code-block:: python

  rho = mas_output['rho']
  rho_r_squared = rho.radial_normalized(2)
  rho_r_squared.plot_phi_cut(...)
