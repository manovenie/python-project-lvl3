import requests
import re

def download(url=url, path):
    r = requests.get(url)
    if r.ok:
        received_html = r.text
        path_to_html = path
        return place_html_to_path(url, received_html, path_to_html)
    pass


def place_html_to_path(url, html, path_to_html):
    # with re url -> file_name
    # create html file at path_to_html
    # write html to that file