import os.path
import shutil

import pytest
from hbutils.testing import isolated_directory, disable_output

from skpick.archive import archive_unpack
from test.testings import get_testfile


@pytest.fixture()
def raw_nested_zip():
    return get_testfile('raw_nested.zip')


@pytest.fixture()
def raw_nested_x_7z():
    return get_testfile('raw_nested_x.7z')


@pytest.mark.unittest
class TestArchiveNested:
    def test_archive_unpack_nested(self, raw_nested_zip, check_unpack_nested_dir):
        with isolated_directory():
            with disable_output():
                for file, relpath in archive_unpack(raw_nested_zip):
                    dst_file = relpath
                    if os.path.dirname(dst_file):
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copyfile(file, dst_file)

            check_unpack_nested_dir('.')

    def test_archive_unpack_nested_x(self, raw_nested_x_7z, check_unpack_nested_x_dir):
        with isolated_directory():
            with disable_output():
                for file, relpath in archive_unpack(raw_nested_x_7z):
                    dst_file = relpath
                    if os.path.dirname(dst_file):
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copyfile(file, dst_file)

            check_unpack_nested_x_dir('.')
