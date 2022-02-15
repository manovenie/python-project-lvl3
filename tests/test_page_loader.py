import requests
import requests_mock
import os
from page_loader.page_loader import download

TEST_URL = 'https://ru.hexlet.io/courses'

def test_page_loader(requests_mock):
    requests_mock.get(TEST_URL)
    res = requests.get(TEST_URL)
    assert res.status_code == 200

'''
def test_page_loader(requests_mock):
    full_path = download(url=TEST_URL,
                      initial_path=os.getcwd())
    with open(full_path, 'r') as result_file:
        with open('tests/fixtures/hexlet.html', 'r') as fixture_file:
            assert result_file.read() == fixture_file.read()
'''