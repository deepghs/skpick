import re

import pytest
from hbutils.random import random_sha1_with_timestamp
from hfutils.operate.base import get_hf_fs, get_hf_client

from test.testings import get_testfile, dir_compare


@pytest.fixture()
def raw_dir():
    return get_testfile('raw')


@pytest.fixture()
def check_unpack_dir(raw_dir):
    def _check(directory):
        dir_compare(raw_dir, directory)

    return _check


@pytest.fixture()
def raw_nested_dir():
    return get_testfile('raw_nested')


@pytest.fixture()
def check_unpack_nested_dir(raw_nested_dir):
    def _check(directory):
        dir_compare(raw_nested_dir, directory)

    return _check


@pytest.fixture()
def raw_nested_x_dir():
    return get_testfile('raw_nested_x')


@pytest.fixture()
def check_unpack_nested_x_dir(raw_nested_x_dir):
    def _check(directory):
        dir_compare(raw_nested_x_dir, directory)

    return _check


_REPO_URL_PATTERN = re.compile(r'^https://huggingface.co/datasets/(?P<repo>[a-zA-Z\d/_\-]+)$')


@pytest.fixture()
def hf_client():
    return get_hf_client()


@pytest.fixture()
def hf_fs():
    return get_hf_fs()


@pytest.fixture()
def hf_repo(hf_client):
    repo_name = f'test_repo_{random_sha1_with_timestamp()}'
    url = hf_client.create_repo(repo_name, repo_type='dataset', exist_ok=True)
    repo_name = _REPO_URL_PATTERN.fullmatch(url).group('repo')
    try:
        yield repo_name
    finally:
        hf_client.delete_repo(repo_name, repo_type='dataset')
