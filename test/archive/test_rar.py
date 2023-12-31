import os.path
import shutil
from unittest import skipUnless

import pytest
from hbutils.testing import isolated_directory, disable_output

from skpick.archive import get_archive_type, get_archive_extname, archive_unpack
from test.testings import get_testfile

try:
    import rarfile
except ImportError:  # pragma: no cover
    rarfile = None


@pytest.fixture()
def raw_rar():
    return get_testfile('raw.rar')


@pytest.mark.unittest
class TestArchiveRar:
    @skipUnless(rarfile, 'rarfile module required.')
    def test_get_archive_type(self):
        assert get_archive_type(os.path.join('1.rar')) == 'rar'
        assert get_archive_type(os.path.join('111', 'f.rar')) == 'rar'

    @skipUnless(not rarfile, 'No rarfile module required.')
    def test_get_archive_type_no_rar(self):
        with pytest.raises(ValueError):
            _ = get_archive_type(os.path.join('1.rar'))
        with pytest.raises(ValueError):
            _ = get_archive_type(os.path.join('111', 'f.rar'))

    @skipUnless(rarfile, 'rarfile module required.')
    def test_get_archive_extname(self):
        assert get_archive_extname('rar') == '.rar'

    @skipUnless(not rarfile, 'No rarfile module required.')
    def test_get_archive_extname_no_rar(self):
        with pytest.raises(ValueError):
            _ = get_archive_extname('rar')

    @skipUnless(rarfile, 'rarfile module required.')
    def test_archive_unpack(self, raw_rar, check_unpack_dir):
        with isolated_directory():
            with disable_output():
                for file, relpath in archive_unpack(raw_rar):
                    dst_file = relpath
                    if os.path.dirname(dst_file):
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copyfile(file, dst_file)
            check_unpack_dir('.')
