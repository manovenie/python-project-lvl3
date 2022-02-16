import pytest
import requests
import requests_mock
import tempfile
import os
from page_loader.page_loader import download
from pathlib import Path, PurePath

TEST_URL = 'https://ru.hexlet.io/courses'
HTML_FIXTURE = 'tests/fixtures/hexlet.html'

def test_page_loader(requests_mock, tmpdir):
    requests_mock.get(TEST_URL)
    real_html = download(TEST_URL, os.getcwd())
    real_page = Path(PurePath(real_html)).read_bytes()
    expected_page = Path(PurePath(HTML_FIXTURE)).read_bytes()
    assert real_page == expected_page

'''
def test_page_loader(requests_mock):
    full_path = download(url=TEST_URL,
                      initial_path=os.getcwd())
    with open(full_path, 'r') as result_file:
        with open('tests/fixtures/hexlet.html', 'r') as fixture_file:
            assert result_file.read() == fixture_file.read()
'''