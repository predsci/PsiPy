"""
Tools for reading pluto model outputs.
"""
import glob
from pathlib import Path


def get_pluto_variables(path):
    """
    Return a list of variables present in a given directory.

    Parameters
    ----------
    path :
        Path to the folder containing the PLUTO data files.

    Returns
    -------
    var_names : list
        List of variable names present in the given directory.
    """
    files = glob.glob(str(Path(path) / '*.dbl'))
    # Get the variable name from the filename
    # Take anything before the . in the first three characters
    var_names = [Path(f).stem[:3].split('.')[0] for f in files]
    # Only return unique names
    var_names = list(set(var_names))
    var_names.sort()
    return var_names
