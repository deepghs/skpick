import os

from hbutils.system import TemporaryDirectory
from hfutils.utils import tqdm

from .base import register_archive_type

try:
    import py7zr
except ImportError:  # pragma: no cover
    py7zr = None


def _7z_unpack(sz_file, silent: bool = False):
    with py7zr.SevenZipFile(sz_file, 'r') as zf:
        progress = tqdm(zf.getnames(), silent=silent, desc=f'Unpacking {sz_file!r} ...')
        for name in progress:
            with TemporaryDirectory() as td:
                progress.set_description(name)
                zf.extract(path=td, targets=[name])
                zf.reset()
                yield os.path.join(td, name), name


if py7zr is not None:
    register_archive_type('7z', ['.7z'], _7z_unpack)
