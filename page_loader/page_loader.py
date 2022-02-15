import requests
import re


def download(url, path):
    r = requests.get(url)
    if r.ok:
        received_html = r.text
        half_path_to_html = path
        return place_html_to_path(url, received_html, half_path_to_html)
    pass


def place_html_to_path(url, html, half_path_to_html):
    url_stripped = re.search(r'(?<=https://).*', url)
    if url_stripped:
        url_without_scheme = url_stripped.group()
        file_name = re.sub(r'[^a-zA-Z0-9]', '-', url_without_scheme) + '.html'
        full_path_to_html = half_path_to_html + file_name
        with open(full_path_to_html, 'w') as file:
            file.write(html)
        return full_path_to_html
