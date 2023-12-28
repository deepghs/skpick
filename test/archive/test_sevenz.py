import os.path
import shutil
from unittest import skipUnless

import pytest
from hbutils.testing import isolated_directory, disable_output

from skpick.archive import get_archive_type, get_archive_extname, archive_unpack
from test.testings import get_testfile

try:
    import py7zr
except ImportError:  # pragma: no cover
    py7zr = None


@pytest.fixture()
def raw_7z():
    return get_testfile('raw.7z')


@pytest.mark.unittest
class TestArchive7z:
    @skipUnless(py7zr, 'py7zr module required.')
    def test_get_archive_type(self):
        assert get_archive_type(os.path.join('1.7z')) == '7z'
        assert get_archive_type(os.path.join('111', 'f.7z')) == '7z'

    @skipUnless(not py7zr, 'No py7zr module required.')
    def test_get_archive_type_no_7z(self):
        with pytest.raises(ValueError):
            _ = get_archive_type(os.path.join('1.7z'))
        with pytest.raises(ValueError):
            _ = get_archive_type(os.path.join('111', 'f.7z'))

    @skipUnless(py7zr, 'py7zr module required.')
    def test_get_archive_extname(self):
        assert get_archive_extname('7z') == '.7z'

    @skipUnless(not py7zr, 'No py7zr module required.')
    def test_get_archive_extname_no_7z(self):
        with pytest.raises(ValueError):
            _ = get_archive_extname('7z')

    @skipUnless(py7zr, 'py7zr module required.')
    def test_archive_unpack(self, raw_7z, check_unpack_dir):
        with isolated_directory():
            with disable_output():
                for file, relpath in archive_unpack(raw_7z):
                    dst_file = relpath
                    if os.path.dirname(dst_file):
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copyfile(file, dst_file)
            check_unpack_dir('.')
