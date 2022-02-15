import argparse
import os


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('-o', '--output', metavar='output_path', default=os.getcwd(),
                        type=str, help='output path that starts with "/')
    parser.add_argument('url', metavar='url', type=str, help='url to parse from')
    return parser.parse_args()