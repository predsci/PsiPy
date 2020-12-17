"""
This file includes global test configuration.

In particular, it defines the location where sample data is available.
"""
from pathlib import Path

import pytest

test_data_dir = (Path(__file__) / '..' / '..' / 'data').resolve()


@pytest.fixture(scope="module", params=['mas_hdf4', 'mas_hdf5'])
def mas_directory(request):
    directory = test_data_dir / request.param
    if not directory.exists():
        pytest.xfail(f'Could not find MAS data directory at {directory}')

    return directory
