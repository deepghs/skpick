import os

from hbutils.system import TemporaryDirectory
from hfutils.utils import tqdm

from .base import register_archive_type

try:
    import rarfile
except ImportError:  # pragma: no cover
    rarfile = None


def _rar_unpack(rar_file, silent: bool = False):
    with rarfile.RarFile(rar_file, 'r') as zf:
        progress = tqdm(zf.namelist(), silent=silent, desc=f'Unpacking {rar_file!r} ...')
        for rarinfo in progress:
            if not zf.getinfo(rarinfo).is_dir():
                with TemporaryDirectory() as td:
                    progress.set_description(rarinfo)
                    zf.extract(rarinfo, td)
                    yield os.path.join(td, rarinfo), rarinfo


if rarfile is not None:
    register_archive_type('rar', ['.rar'], _rar_unpack)
