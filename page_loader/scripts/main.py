# !/usr/bin/env python3
from page_loader.cli import parse_cli_args
from page_loader.page_loader import download


def main():
    arguments = parse_cli_args() # .output_path & .url
    page = download(url=arguments.url, path=arguments.output_path)
    print(page) # NB! print path


if __name__ == '__main__':
    main()
