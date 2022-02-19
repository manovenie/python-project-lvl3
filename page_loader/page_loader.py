import requests
import re
import os
from bs4 import BeautifulSoup


WANTED_TAGS = ('img')


def download(url, initial_path):
    html_page = get_html_page(url)
    html_page_path = create_name_or_path(url, initial_path, ext='.html')
    resource_path = create_name_or_path(url, initial_path, ext='_files')
    os.mkdir(resource_path)
    html = prepare_soup(html_page, resource_path)
    write_file_to_path(html_page_path, html.encode())
    return html_page_path


def prepare_soup(html_page, resource_path):
    soup = BeautifulSoup(html_page, 'html.parser')
    images = soup.find_all('img')
    html = soup.prettify(formatter='html5')
    for img in images:
        link = img['src']
        img_bytes = requests.get(link).content
        img_name = create_name_or_path(link, resource_path, path_needed=False)
        full_path = resource_path + '/' + img_name
        write_file_to_path(full_path, img_bytes)
        soup_html = BeautifulSoup(html, 'html.parser')
        html_image = soup_html.find('img')
        html_image['src'] = full_path
        print(html_image['src'])
    return html


def get_html_page(url):
    response = requests.get(url)
    if response.ok:
        return response.text


def create_name_or_path(url, initial_path, ext=None, path_needed=True):
    url_stripped = re.search(r'(?<=https://).*', url)
    if url_stripped:
        url_without_scheme = url_stripped.group()
        if path_needed:
            file_name = format_str(url_without_scheme)
            full_path = initial_path + '/' + file_name + ext
            return full_path
        return format_resource(url_without_scheme)


def format_str(string):
    return re.sub(r'[^a-zA-Z0-9]', '-', string)


def format_resource(string):
    base = '-'.join(string.split('.')[:-1])
    string = base + '.png'
    return re.sub(r'/', '-', string)


def write_file_to_path(full_path, file):
    with open(full_path, 'wb') as f:
        f.write(file)
