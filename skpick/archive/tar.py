import os.path
import tarfile
from typing import Literal

from hbutils.system import TemporaryDirectory
from hfutils.utils import tqdm

from .base import register_archive_type
from .zip import _ZLIB_SUPPORTED

try:
    import bz2

    del bz2
    _BZ2_SUPPORTED = True
except ImportError:
    _BZ2_SUPPORTED = False

try:
    import lzma

    del lzma
    _LZMA_SUPPORTED = True
except ImportError:
    _LZMA_SUPPORTED = False

CompressTyping = Literal['', 'gzip', 'bzip2', 'xz']


def _tarfile_unpack(tar_file, silent: bool = False, numeric_owner=False):
    with tarfile.open(tar_file) as tar:
        progress = tqdm(tar, silent=silent, desc=f'Unpacking {tar_file!r} ...')
        for tarinfo in progress:
            progress.set_description(tarinfo.name)
            if not tarinfo.isdir():
                with TemporaryDirectory() as td:
                    tar.extract(tarinfo, td, set_attrs=False, numeric_owner=numeric_owner)
                    yield os.path.join(td, tarinfo.name), tarinfo.name


register_archive_type('tar', ['.tar'], _tarfile_unpack)
if _ZLIB_SUPPORTED:
    register_archive_type('gztar', ['.tar.gz', '.tgz'], _tarfile_unpack)
if _BZ2_SUPPORTED:
    register_archive_type('bztar', ['.tar.bz2', '.tbz2'], _tarfile_unpack)
if _LZMA_SUPPORTED:
    register_archive_type('xztar', ['.tar.xz', '.txz'], _tarfile_unpack)
