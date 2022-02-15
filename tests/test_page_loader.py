import requests
import requests_mock
from page_loader.page_loader import download

def test_page_loader():
    assert 2 == 2

    file_path = download(url=url, path=output_path)
    print(file_path)