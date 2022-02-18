import requests
import re
import os
from bs4 import BeautifulSoup


WANTED_TAGS = ('img')


def download(url, initial_path):
    html_page = get_html_page(url)
    html_page_path = generate_full_path(url, initial_path, extension='.html')
    # write_file_to_path(html_path, html_page)
    # create folder for img
    resource_path = generate_full_path(url, initial_path, extension='_files')
    html, resources = prepare_soup(html_page, url, resource_path)

    # os.mkdir(img_folder)
    # scan all imgs, loop over to get names of imgs,
    # download img via tags and write them in folder
    # soup = BeautifulSoup(r.text, 'html.parser')
    # images = soup.find_all('img')
    # change links to imgs in generated file
    return html_page_path


def prepare_soup(html_page, url, resource_path):
    soup = BeautifulSoup(html_page, 'html.parser')
    wanted_items = soup.find_all(WANTED_TAGS)


def get_html_page(url):
    response = requests.get(url)
    if response.ok:
        return response.text


def generate_full_path(url, initial_path, extension=None):
    url_stripped = re.search(r'(?<=https://).*', url)
    if url_stripped:
        url_without_scheme = url_stripped.group()
        file_name = re.sub(r'[^a-zA-Z0-9]', '-', url_without_scheme)
        full_path = initial_path + '/' + file_name + extension
        return full_path
    return None


def write_file_to_path(full_path, file):
    with open(full_path, 'wb') as f:
        f.write(file)
