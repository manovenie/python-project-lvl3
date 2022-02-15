# !/usr/bin/env python3
from page_loader.cli import parse_cli_args
from page_loader.page_loader import download


def main():
    arguments = parse_cli_args()
    url = arguments.URL
    output_path = arguments.output
    file_path = download(url=url, path=output_path)
    print(file_path)


if __name__ == '__main__':
    main()
