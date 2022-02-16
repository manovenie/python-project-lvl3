import requests
import re


def download(url, initial_path):
    r = requests.get(url)
    if r.ok:
        received_html = r.content
        full_path = generate_full_path(url, initial_path)
        write_file_to_path(full_path, received_html)
        return full_path
    return None


def generate_full_path(url, initial_path):
    url_stripped = re.search(r'(?<=https://).*', url)
    if url_stripped:
        url_without_scheme = url_stripped.group()
        file_name = re.sub(r'[^a-zA-Z0-9]', '-', url_without_scheme) + '.html'
        full_path = initial_path + '/' + file_name
        return full_path
    return None


def write_file_to_path(full_path, html):
    with open(full_path, 'wb') as file:
        file.write(html)
