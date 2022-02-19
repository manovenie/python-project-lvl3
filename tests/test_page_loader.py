#!/usr/bin/env python3

from page_loader import download
from page_loader.page_loader import format_local_name, upload_files
import tempfile
import pytest
import os


@pytest.mark.parametrize('URL, get_name, file_status, dir_status,', [
    ('https://github.com/dutlov/python-project-lvl3',
     'github-com-dutlov-python-project-lvl3.html', None, None),
    ('https://github.com/dutlov/python-project-lvl3',
     'github-com-dutlov-python-project-lvl3_files', None, True),
    ('https://github.com/dutlov/python-project-lvl3.css',
     'github-com-dutlov-python-project-lvl3.css', True, None)
])
def test_get_name(URL, get_name, dir_status, file_status):
    assert format_local_name(URL, file=file_status,
                             dir=dir_status) == get_name


def test_load_files():
    with tempfile.TemporaryDirectory() as temp:
        link_for_test = 'https://github.com/dutlov/python-project-lvl3'
        path = os.path.join(temp, format_local_name(link_for_test, 'file'))
        upload_files([(link_for_test, path)])
        assert os.path.isfile(path)


@pytest.mark.parametrize('URL, path, exception', [
    ('dutlov.github.io/github.io/', '/error_path/', 'Wrong address!'),
    ('ht://dutlov.github.io/github.io/', '/error_path/', 'Wrong address!'),
    ('http://httpdqwasd.org/status/404', '/error_path/', 'Connection failed'),
    ('https://github.com/dutlov/python-project-lvl3',
     'error_path', 'Your folder is incorrect')
])
def test_errors(URL, path, exception):
    with pytest.raises(Exception):
        download(URL, path)
