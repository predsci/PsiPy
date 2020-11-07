import pyhdf.SD as h4


__all__ = ['HDF4File']


class HDF4File:
    """
    A context manager for opening/closing HDF4 files
    """
    def __init__(self, file_name):
        file_name = str(file_name)
        self.file_obj = h4.SD(file_name)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.end()
