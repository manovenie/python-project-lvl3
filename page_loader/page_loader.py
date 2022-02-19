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
    os.mkdir(path_files_folder)
    edited_page, resources = \
        edit_page_and_get_links(html_page, url, path_files_folder)
    save_file(edited_page, path_page)
    upload_files(resources)
    return path_page


def is_local(pointer, url):
    first = urlparse(url).netloc
    second = urlparse(urljoin(url, pointer)).netloc
    return first == second


def edit_page_and_get_links(html_page, url, path_files_folder):
    dir_path, dir_name = os.path.split(path_files_folder)
    soup = BeautifulSoup(html_page, 'html.parser')
    elements = [item for item in soup.find_all(list(WANTED_TAGS))
                if is_local(item.get(WANTED_TAGS[item.name]), url)]
    links = []
    for element in elements:
        tag = WANTED_TAGS[element.name]
        link = urljoin(url, element.get(tag, ''))
        if not os.path.splitext(link)[1]:
            resource_path = os.path.join(dir_name, format_local_name(link))
        else:
            resource_path = \
                os.path.join(dir_name, format_local_name(link, file=True))
        element[tag] = resource_path
        links.append((link, os.path.join(dir_path, resource_path)))
    edited_page = soup.prettify("utf-8")
    return edited_page, links


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


def save_file(data, path):
    with open(path, 'wb') as file:
        file.write(data)


def upload_files(source):
    for link, path in source:
        r = requests.get(link)
        data = r.content
        save_file(data, path)
