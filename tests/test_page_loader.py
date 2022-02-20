#!/usr/bin/env python3

from page_loader import download
from page_loader.page_loader import format_local_name, upload_files
import tempfile
import pytest
import os

URL_TEST = 'https://gov.uk/'

PATH_FIXTURES_MOCK_lINKS = {
    'tests/fixtures/test_page.html': 'https://gov.uk/',
    'tests/fixtures/test_css.css': 'https://www.gov.uk/assets/static/application-eeefd93bb4e3a40533688e62bae6a241ff74802cba07f6da687198e517c4b13e.css',
    'tests/fixtures/test_svg.svg': 'https://www.gov.uk/assets/static/govuk-mask-icon-de738c3fcce8ce2a91b67e89787090dc24a5cda0275ab6b75f6226c5b9619d3d.svg',
}

LOCAL_PATH_NAME = (
    'www-gov-uk_files/www-gov-uk.html',
    'www-gov-uk_files/www-gov-uk-assets-static-application-eeefd93bb4e3a40533688e62bae6a241ff74802cba07f6da687198e517c4b13e.css',
    'www-gov-uk_files/www-gov-uk-assets-static-govuk-mask-icon-de738c3fcce8ce2a91b67e89787090dc24a5cda0275ab6b75f6226c5b9619d3d.svg',
)


def test_downloader(requests_mock):
    with tempfile.TemporaryDirectory() as temp:
        for fixture, link in PATH_FIXTURES_MOCK_lINKS.items():
            with open(fixture, 'rb') as fixture_file:
                mocking_content = fixture_file.read()
            requests_mock.get(link, content=mocking_content)
        path_load_page = download(URL_TEST, temp)

        with open(os.path.join(temp, path_load_page)) as test_page:
            with open('tests/fixtures/test_page.html') as fixture_page:
                assert test_page.read() == fixture_page.read()

        local_files = [os.path.join(temp, file) for file in LOCAL_PATH_NAME]

        for fixture, local in zip(PATH_FIXTURES_MOCK_lINKS, local_files):
            with open(fixture, 'rb') as fixture_file:
                with open(local, 'rb') as load_file:
                    assert fixture_file.read() == load_file.read()


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
