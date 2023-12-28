import os.path
import zipfile
from tempfile import TemporaryDirectory

from hfutils.utils import tqdm

from .base import register_archive_type

try:
    import zlib

    del zlib
    _ZLIB_SUPPORTED = True
except ImportError:
    _ZLIB_SUPPORTED = False


def _zip_unpack(zip_file, silent: bool = False):
    with zipfile.ZipFile(zip_file, 'r') as zf:
        progress = tqdm(zf.namelist(), silent=silent, desc=f'Unpacking {zip_file!r} ...')
        for zipinfo in progress:
            with TemporaryDirectory() as td:
                progress.set_description(zipinfo)
                zf.extract(zipinfo, td)
                yield os.path.join(td, zipinfo), os.path.join(zipinfo)


if _ZLIB_SUPPORTED:
    register_archive_type('zip', ['.zip'], _zip_unpack)
