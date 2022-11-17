import numpy as np
import pyhdf.SD as h4
import h5py as h5

def rdh5(h5_filename):
    x = np.array([])
    y = np.array([])
    z = np.array([])
    f = np.array([])

    h5file = h5.File(h5_filename, 'r')
    f = h5file['Data']
    dims = f.shape
    ndims = np.ndim(f)

    #Get the scales if they exist:
    for i in range(0,ndims):
        if i == 0:
            if (len(h5file['Data'].dims[0].keys())!=0):
                x = h5file['Data'].dims[0][0]
        elif i == 1:
            if (len(h5file['Data'].dims[1].keys())!=0):
                y = h5file['Data'].dims[1][0]
        elif i == 2:
            if (len(h5file['Data'].dims[2].keys())!=0):
                z = h5file['Data'].dims[2][0]

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    f = np.array(f)

    h5file.close()

    return (x,y,z,f)

def rdhdf(hdf_filename):

    if (hdf_filename.endswith('h5')):
        x,y,z,f = rdh5(hdf_filename)
        return (x,y,z,f)

    x = np.array([])
    y = np.array([])
    z = np.array([])
    f = np.array([])

    # Open the HDF file
    sd_id = h4.SD(hdf_filename)

    #Read dataset.  In all PSI hdf4 files, the
    #data is stored in "Data-Set-2":
    sds_id = sd_id.select('Data-Set-2')
    f = sds_id.get()

    #Get number of dimensions:
    ndims = np.ndim(f)

    # Get the scales. Check if theys exist by looking at the 3rd
    # element of dim.info(). 0 = none, 5 = float32, 6 = float64.
    # see http://pysclint.sourceforge.net/pyhdf/pyhdf.SD.html#SD
    # and http://pysclint.sourceforge.net/pyhdf/pyhdf.SD.html#SDC
    for i in range(0,ndims):
        dim = sds_id.dim(i)
        if dim.info()[2] != 0:
            if i == 0:
                x = dim.getscale()
            elif i == 1:
                y = dim.getscale()
            elif i == 2:
                z = dim.getscale()

    sd_id.end()

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    f = np.array(f)

    return (x,y,z,f)

def rdhdf_1d(hdf_filename):

    x,y,z,f = rdhdf(hdf_filename)

    return (x,f)

def rdhdf_2d(hdf_filename):

    x,y,z,f = rdhdf(hdf_filename)

    if (hdf_filename.endswith('h5')):
        return(x,y,f)
    return (y,x,f)

def rdhdf_3d(hdf_filename):

    x,y,z,f = rdhdf(hdf_filename)
    if (hdf_filename.endswith('h5')):
        return(x,y,z,f)

    return (z,y,x,f)

def wrh5(h5_filename, x, y, z, f):

    h5file = h5.File(h5_filename, 'w')

    # Create the dataset (Data is the name used by the psi data)).
    h5file.create_dataset("Data", data=f)

    # Make sure the scales are desired by checking x type, which can
    # be None or None converted by np.asarray (have to trap seperately)
    if x is None: 
        x = np.array([], dtype=f.dtype)
        y = np.array([], dtype=f.dtype)
        z = np.array([], dtype=f.dtype)
    if x.any() == None:
        x = np.array([], dtype=f.dtype)
        y = np.array([], dtype=f.dtype)
        z = np.array([], dtype=f.dtype)

    # Make sure scales are the same precision as data.
    x=x.astype(f.dtype)
    y=y.astype(f.dtype)
    z=z.astype(f.dtype)

    #Get number of dimensions:
    ndims = np.ndim(f)

    #Set the scales:
    for i in range(0,ndims):
        if i == 0 and len(x) != 0:
            dim = h5file.create_dataset("dim1", data=x)
#            h5file['Data'].dims.create_scale(dim,'dim1')
            dim.make_scale('dim1')
            h5file['Data'].dims[0].attach_scale(dim)
            h5file['Data'].dims[0].label = 'dim1'
        if i == 1 and len(y) != 0:
            dim = h5file.create_dataset("dim2", data=y)
#            h5file['Data'].dims.create_scale(dim,'dim2')
            dim.make_scale('dim2')
            h5file['Data'].dims[1].attach_scale(dim)
            h5file['Data'].dims[1].label = 'dim2'
        elif i == 2 and len(z) != 0:
            dim = h5file.create_dataset("dim3", data=z)
#            h5file['Data'].dims.create_scale(dim,'dim3')
            dim.make_scale('dim3')
            h5file['Data'].dims[2].attach_scale(dim)
            h5file['Data'].dims[2].label = 'dim3'

    # Close the file:
    h5file.close()

def wrhdf(hdf_filename, x, y, z, f):

    if (hdf_filename.endswith('h5')):
        wrh5(hdf_filename, x, y, z, f)
        return

    # Create an HDF file
    sd_id = h4.SD(hdf_filename, h4.SDC.WRITE | h4.SDC.CREATE | h4.SDC.TRUNC)

    # Due to bug, need to only write 64-bit.
    f = f.astype(np.float64)
    ftype = h4.SDC.FLOAT64

#    if f.dtype == np.float32:
#        ftype = h4.SDC.FLOAT32
#    elif f.dtype == np.float64:
#        ftype = h4.SDC.FLOAT64

    # Create the dataset (Data-Set-2 is the name used by the psi data)).
    sds_id = sd_id.create("Data-Set-2", ftype, f.shape)

    #Get number of dimensions:
    ndims = np.ndim(f)

    # Make sure the scales are desired by checking x type, which can
    # be None or None converted by np.asarray (have to trap seperately)
    if x is None: 
        x = np.array([], dtype=f.dtype)
        y = np.array([], dtype=f.dtype)
        z = np.array([], dtype=f.dtype)
    if x.any() == None:
        x = np.array([], dtype=f.dtype)
        y = np.array([], dtype=f.dtype)
        z = np.array([], dtype=f.dtype)

    # Due to python hdf4 bug, need to use double scales only.

    x=x.astype(np.float64)
    y=y.astype(np.float64)
    z=z.astype(np.float64)

    #Set the scales (or don't if x is none or length zero)
    for i in range(0,ndims):
        dim = sds_id.dim(i)
        if i == 0 and len(x) != 0:
            if x.dtype == np.float32:
                stype = h4.SDC.FLOAT32
            elif x.dtype == np.float64:
                stype = h4.SDC.FLOAT64
            dim.setscale(stype,x)
        elif i == 1  and len(y) != 0:
            if y.dtype == np.float32:
                stype = h4.SDC.FLOAT32
            elif y.dtype == np.float64:
                stype = h4.SDC.FLOAT64
            dim.setscale(stype,y)
        elif i == 2 and len(z) != 0:
            if z.dtype == np.float32:
                stype = h4.SDC.FLOAT32
            elif z.dtype == np.float64:
                stype = h4.SDC.FLOAT64
            dim.setscale(stype,z)

    # Write the data:
    sds_id.set(f)

    # Close the dataset:
    sds_id.endaccess()

    # Flush and close the HDF file:
    sd_id.end()


def wrhdf_1d(hdf_filename,x,f):

    x = np.asarray(x)
    y = np.array([])
    z = np.array([])
    f = np.asarray(f)
    wrhdf(hdf_filename,x,y,z,f)


def wrhdf_2d(hdf_filename,x,y,f):

    x = np.asarray(x)
    y = np.asarray(y)
    z = np.array([])
    f = np.asarray(f)
    if (hdf_filename.endswith('h5')):
        wrhdf(hdf_filename,x,y,z,f)
        return
    wrhdf(hdf_filename,y,x,z,f)


def wrhdf_3d(hdf_filename,x,y,z,f):

    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    f = np.asarray(f)
    if (hdf_filename.endswith('h5')):
        wrhdf(hdf_filename,x,y,z,f)
        return
    wrhdf(hdf_filename,z,y,x,f)

