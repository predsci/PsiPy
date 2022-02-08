"""
Helper functions for downloading sample model output data.
"""
from pathlib import Path

from parfive import Downloader

download_dir = Path(__file__).parent / '..' / '..' / 'data'
data_url = 'http://www.predsci.com/data/runs'


def get_mas_helio_dir():
    mas_helio_dir = download_dir / 'mas_helio'
    mas_helio_dir.mkdir(parents=True, exist_ok=True)
    return mas_helio_dir.resolve()


def mas_helio():
    """
    Get some MAS heliospheric data files. These are taken from CR2210, which
    is used for PSP data comparisons in the documentation examples.

    Returns
    -------
    pathlib.Path
        Download directory.
    """
    mas_helio_dir = get_mas_helio_dir()
    base_url = (f'{data_url}/cr2210-medium/hmi_masp_mas_std_0201/helio/'
                '{var}002.hdf')

    # Create a downloader to queue the files to be downloaded
    dl = Downloader()
    for var in ['rho', 'vr', 'br']:
        file = mas_helio_dir / f'{var}002.hdf'
        if file.exists():
            continue
        else:
            remote_file = base_url.format(var=var)
            dl.enqueue_file(remote_file, path=mas_helio_dir)

    # Download the files
    if dl.queued_downloads > 0:
        result = dl.download()
        if len(result.errors):
            raise RuntimeError(
                'Failed to download files with the following errors:'
                f'{result.errors}')
    return mas_helio_dir


def mas_helio_timesteps():
    """
    Get two MAS heliospheric data files for two subsequent Carrington
    rotations.

    This is used as sample data for animations - animations are intended to be
    used with output from time dependent simulations, but for ease of
    downloading sample data here we pretend that two Carrington rotations are
    time animations.

    Returns
    -------
    pathlib.Path
        Download directory.
    """
    mas_helio_dir = get_mas_helio_dir()
    mas_anim_dir = mas_helio_dir / 'animation'
    base_url = (data_url +
                '/cr{cr}-medium/hmi_masp_mas_std_0201/helio/vr002.hdf')

    # Create a downloader to queue the files to be downloaded
    dl = Downloader()
    for i, cr in enumerate([2210, 2211]):
        fname = f'vr00{i+1}.hdf'
        file = mas_anim_dir / fname
        if file.exists():
            continue
        else:
            remote_file = base_url.format(cr=cr)
            dl.enqueue_file(remote_file, path=mas_anim_dir, filename=fname)

    # Download the files
    if dl.queued_downloads > 0:
        dl.download()
    return mas_anim_dir
