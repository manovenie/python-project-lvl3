import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


WANTED_TAGS = {'link': 'href', 'img': 'src', 'script': 'src'}


def download(url, cli_path):
    html_page = load_page(url)
    name_page = format_local_name(url)
    path_page = os.path.join(cli_path, name_page)
    name_files_folder = format_local_name(url, dir=True)
    path_files_folder = os.path.join(cli_path, name_files_folder)
    os.mkdir(path_folder)
    edited_page, resources = get_links_and_edit_page(html_page, url, path_files_folder)

    return html_page_path


def edit_page_and_get_links(html_page, url, path_files_folder):
    dir_path, dir_name = os.path.split(path_files_folder)
    soup = BeautifulSoup(html_page, 'html.parser')
    elements = [item for items in soup.find_all(list(WANTED_TAGS))]
    result = []
    images = soup.find_all('img')
    html = soup.prettify(formatter='html5')
    for img in images:
        link = img['src']
        img_bytes = requests.get(link).content
        img_name = format_local_name(link, resource_path)
        full_path = resource_path + '/' + img_name
        write_file_to_path(full_path, img_bytes)
        soup_html = BeautifulSoup(html, 'html.parser')
        html_image = soup_html.find('img')
        html_image['src'] = full_path
        print(html_image['src'])
    return html


def load_page(url):
    response = requests.get(url)
    if response.ok:
        return response.text


def format_local_name(url, file=None, dir=None):
    link = url.rstrip('/')
    o = urlparse(link)
    name = o.netloc + o.path
    if file:
        name, name_ext = os.path.splitext(name)
    final_name = re.sub(r'\W', '-', name)
    if file:
        final_name += name_ext
    elif dir:
        final_name += '_files'
    else:
        final_name += '.html'
    return final_name


def format_resource(string):
    base = '-'.join(string.split('.')[:-1])
    string = base + '.png'
    return re.sub(r'/', '-', string)


def write_file_to_path(full_path, file):
    with open(full_path, 'wb') as f:
        f.write(file)
