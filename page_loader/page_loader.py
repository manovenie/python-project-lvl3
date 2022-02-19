import requests
import re
import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from progress.bar import IncrementalBar


logger = logging.getLogger(__name__)
WANTED_TAGS = {'link': 'href', 'img': 'src', 'script': 'src'}


def download(url, cli_path):
    bar = IncrementalBar('Loading page', max=5, suffix='%(percent)d%%')
    html_page = load_page(url)
    bar.next()
    name_page = format_local_name(url)
    path_page = os.path.join(cli_path, name_page)
    bar.next()
    name_files_folder = format_local_name(url, dir=True)
    path_files_folder = os.path.join(cli_path, name_files_folder)
    bar.next()
    create_dir(path_files_folder)
    bar.next()
    edited_page, resources = \
        edit_page_and_get_links(html_page, url, path_files_folder)
    bar.next()
    save_file(edited_page, path_page)
    bar.next()
    upload_files(resources)
    bar.finish()
    logger.debug('Page and resources loaded')
    return path_page


def is_local(pointer, url):
    logging.info('Checking if file is local')
    first = urlparse(url).netloc
    second = urlparse(urljoin(url, pointer)).netloc
    return first == second


def edit_page_and_get_links(html_page, url, path_files_folder):
    logging.info('Editing page and getting links for wanted tags')
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


def create_dir(path):
    logging.info('Checking for the directory -> creating it')
    try:
        os.mkdir(path)
    except IOError as e:
        raise Exception('Your folder is incorrect') from e


def load_page(url):
    logging.info('Loading page and getting response')
    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema) as e:
        raise Exception('Wrong address') from e
    except requests.exceptions.HTTPError as e:
        raise Exception('Connection failed') from e
    except requests.exceptions.ConnectionError as e:
        raise Exception('Connection error') from e
    return response.text


def format_local_name(url, file=None, dir=None):
    logging.info('Formatting a name')
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


def save_file(data, path):
    logging.info('Writing binary info to file, saving it')
    try:
        with open(path, 'wb') as file:
            file.write(data)
    except IOError as e:
        raise Exception('Your folder is incorrect') from e


def upload_files(source):
    logging.info('Uploading resources from page to local folder')
    bar = IncrementalBar('Uploading files', max=len(source))
    for link, path in source:
        try:
            r = requests.get(link)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception('Connection failed') from e
        else:
            data = r.content
            save_file(data, path)
            bar.next()
        finally:
            continue
    bar.finish()
