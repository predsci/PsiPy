from psipy.io.pot3d import get_pot3d_variables, read_pot3d
from psipy.model import ModelOutput

__all__ = ["POT3DOutput"]


class POT3DOutput(ModelOutput):
    """
    The results from a single run of POT3D.

    This is a storage object that contains a number of `Variable` objects. It
    is designed to be used like::

        mas_output = POT3DOutput('directory')
        br = mas_output['br']

    Notes
    -----
    Variables are loaded on demand. To see the list of available variables
    use `POT3DOutput.variables`, and to see the list of already loaded variables
    use `POT3DOutput.loaded_variables`.
    """

    def get_unit(self, var):
        # TODO: fill in
        ...

    def get_runit(self):
        # TODO: fill in
        ...

    def get_variables(self):
        return get_pot3d_variables(self.path)

    def load_file(self, var):
        return read_pot3d(self.path / (var + ".hdf"))

    def __repr__(self):
        return f'psipy.model.pot3d.POT3DOutput("{self.path}")'

    def __str__(self):
        return f"POT3D output in directory {self.path}\n" + super().__str__()
