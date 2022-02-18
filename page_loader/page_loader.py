import requests
import re
import os
from bs4 import BeautifulSoup


WANTED_TAGS = ('img')


def download(url, initial_path):
    html_page = get_html_page(url)
    html_page_path = generate_name_or_path(url, initial_path, extension='.html')
    # url_formatted = generate_name_or_path(url, initial_path)
    # create folder for img
    resource_path = generate_name_or_path(url, initial_path, extension='_files')
    os.mkdir(resource_path)
    html = prepare_soup(html_page, resource_path)
    write_file_to_path(html_page_path, html.encode())
    # os.mkdir(img_folder)
    # scan all imgs, loop over to get names of imgs,
    # download img via tags and write them in folder
    # soup = BeautifulSoup(r.text, 'html.parser')
    # images = soup.find_all('img')
    # change links to imgs in generated file
    return html_page_path


def prepare_soup(html_page, resource_path):
    soup = BeautifulSoup(html_page, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        link = image['src']
        image_bytes = requests.get(link).content
        image_name = generate_name_or_path(link, resource_path, path_needed=False)
        full_path = resource_path + '/' + image_name
        write_file_to_path(full_path, image_bytes)
    html = soup.prettify(formatter='html5')
    return html


def get_html_page(url):
    response = requests.get(url)
    if response.ok:
        return response.text


def generate_name_or_path(url, initial_path, extension=None, path_needed=True):
    url_stripped = re.search(r'(?<=https://).*', url)
    if url_stripped:
        url_without_scheme = url_stripped.group()
        if path_needed:
            file_name = format_str(url_without_scheme)
            full_path = initial_path + '/' + file_name + extension
            return full_path
        return format_resource(url_without_scheme)


def format_str(string):
    return re.sub(r'[^a-zA-Z0-9]', '-', string)


def format_resource(string):
    base = string.split('.')[:-1]
    base = ''.join(base)
    ext = string.split('.')[1:]
    ext = ''.join(ext)
    string = base + '.' + ext
    return re.sub(r'/', '-', string)


def write_file_to_path(full_path, file):
    with open(full_path, 'wb') as f:
        f.write(file)
