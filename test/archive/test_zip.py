import os.path
import shutil

import pytest
from hbutils.testing import isolated_directory, disable_output

from skpick.archive import get_archive_type, get_archive_extname, archive_unpack
from test.testings import get_testfile


@pytest.fixture()
def raw_zip():
    return get_testfile('raw.zip')


@pytest.mark.unittest
class TestArchiveZip:
    def test_get_archive_type(self):
        assert get_archive_type(os.path.join('1.zip')) == 'zip'
        assert get_archive_type(os.path.join('111', 'f.zip')) == 'zip'

    def test_get_archive_extname(self):
        assert get_archive_extname('zip') == '.zip'

    def test_archive_unpack(self, raw_zip, check_unpack_dir):
        with isolated_directory():
            with disable_output():
                for file, relpath in archive_unpack(raw_zip):
                    dst_file = relpath
                    if os.path.dirname(dst_file):
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copyfile(file, dst_file)

            check_unpack_dir('.')
