#!/usr/bin/env python3

from page_loader import download
from page_loader.page_loader import format_local_name, upload_files
from pathlib import Path, PurePath
from bs4 import BeautifulSoup
import tempfile
import pytest
import os


URL_TEST = 'https://gov.uk/'

PATH_FIXTURES_MOCK_lINKS = {
    'tests/fixtures/test_css.css': 'https://www.gov.uk/assets/static/application-eeefd93bb4e3a40533688e62bae6a241ff74802cba07f6da687198e517c4b13e.css',
    'tests/fixtures/test_svg.svg': 'https://www.gov.uk/assets/static/govuk-mask-icon-de738c3fcce8ce2a91b67e89787090dc24a5cda0275ab6b75f6226c5b9619d3d.svg',
}

LOCAL_PATH_NAME = (
    'www-gov-uk_files/www-gov-uk-assets-static-application-eeefd93bb4e3a40533688e62bae6a241ff74802cba07f6da687198e517c4b13e.css',
    'www-gov-uk_files/www-gov-uk-assets-static-govuk-mask-icon-de738c3fcce8ce2a91b67e89787090dc24a5cda0275ab6b75f6226c5b9619d3d.svg',
)


@pytest.fixture()
def files():
    page_path = Path(PurePath('tests/fixtures/test_page.html'))
    image_path = Path(PurePath('tests/fixtures/test_svg.svg'))
    link_path = Path(PurePath('tests/fixtures/test_css.css'))
    return {
        'page': page_path.read_bytes(),
        'image': image_path.read_bytes(),
        'link': link_path.read_bytes(),
    }


def test_download_html(tmpdir, requests_mock, files):
    requests_mock.get(URL_TEST, content=files['page'])
    requests_mock.get(PATH_FIXTURES_MOCK_lINKS['tests/fixtures/test_svg.svg'], content=files['image'])
    # requests_mock.get('/assets/professions/python.png', content=files['image'])
    requests_mock.get(PATH_FIXTURES_MOCK_lINKS['tests/fixtures/test_css.css'], content=files['link'])
    # requests_mock.get('/assets/application.css', content=files['link'])

    actual_html = download(URL_TEST, tmpdir)
    actual_page = Path(PurePath(actual_html)).read_bytes()
    expected_page = files['page']
    apb = BeautifulSoup(actual_page, 'lxml').prettify(formatter='html5')
    epb = BeautifulSoup(expected_page, 'lxml').prettify(formatter='html5')
    assert epb == apb


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
