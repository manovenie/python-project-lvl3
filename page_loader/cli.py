import argparse
import os


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('-o', '--output',
                        default=os.getcwd(), type=str,
                        help='folder for saving html')
    parser.add_argument('URL', type=str,
                        help='url to parse from')
    return parser.parse_args()
