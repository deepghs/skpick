import os.path
import shutil

import pytest
from hbutils.testing import isolated_directory, disable_output

from skpick.archive import get_archive_type, get_archive_extname, archive_unpack
from test.testings import get_testfile


@pytest.fixture()
def raw_tar():
    return get_testfile('raw.tar')


@pytest.mark.unittest
class TestArchiveTar:
    def test_get_archive_type(self):
        assert get_archive_type(os.path.join('1.tar')) == 'tar'
        assert get_archive_type(os.path.join('111', 'f.tar')) == 'tar'

    def test_get_archive_extname(self):
        assert get_archive_extname('tar') == '.tar'

    @pytest.mark.parametrize(['type_', 'ext'], [
        ('tar', '.tar'),
        ('gztar', '.tar.gz'),
        ('bztar', '.tar.bz2'),
        ('xztar', '.tar.xz'),
    ])
    def test_archive_unpack(self, check_unpack_dir, type_, ext):
        with isolated_directory():
            with disable_output():
                for file, relpath in archive_unpack(get_testfile(f'raw{ext}')):
                    dst_file = relpath
                    if os.path.dirname(dst_file):
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copyfile(file, dst_file)
            check_unpack_dir('.')
