import os

import pytest

from skpick.archive import get_archive_type, get_archive_extname, register_archive_type


@pytest.mark.unittest
class TestArchiveBase:
    def test_get_archive_type(self):
        assert get_archive_type(os.path.join('1.zip')) == 'zip'
        assert get_archive_type(os.path.join('111', 'f.zip')) == 'zip'

        with pytest.raises(ValueError):
            _ = get_archive_type('1.mp3')
        with pytest.raises(ValueError):
            _ = get_archive_type('')

    def test_get_archive_extname(self):
        assert get_archive_extname('zip') == '.zip'
        with pytest.raises(ValueError):
            _ = get_archive_extname('mp3')
        with pytest.raises(ValueError):
            _ = get_archive_extname('')

    def test_empty_register(self):
        with pytest.raises(ValueError):
            register_archive_type('xxx', [], lambda: None)
