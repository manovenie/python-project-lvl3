# !/usr/bin/env python3
from page_loader.cli import parse_cli_args
from page_loader.page_loader import download


def main():
    arguments = parse_cli_args()
    page = download(url=arguments.url, path=arguments.output_path)
    print(page)


if __name__ == '__main__':
    main()
