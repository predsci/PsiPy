"""
Helper functions for downloading sample model output data.
"""
from pathlib import Path

from parfive import Downloader

download_dir = Path(__file__).parent / '..' / '..' / 'data'


def mas_helio():
    """
    Get some MAS heliospheric data files. These are taken from CR2210, which
    is used for the PSP data comparisons.
    """
    mas_helio_dir = download_dir / 'mas_helio'
    mas_helio_dir.mkdir(parents=True, exist_ok=True)
    base_url = 'http://www.predsci.com/data/runs/cr2210-medium/hmi_masp_mas_std_0201/helio/{var}002.hdf'

    # Create a downloader to queue the files to be downloaded
    dl = Downloader()

    vars = ['rho', 'vr']
    for var in vars:
        file = mas_helio_dir / f'{var}002.hdf'
        if file.exists():
            continue
        else:
            remote_file = base_url.format(var=var)
            dl.enqueue_file(remote_file, path=mas_helio_dir)

    # Download the files
    if dl.queued_downloads > 0:
        dl.download()
    return mas_helio_dir.resolve()
