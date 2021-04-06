import argparse

from chucknorris_cli.quips import quip

def parse_args():
    parser = argparse.ArgumentParser(description='The finest selection of Chuck Norris jokes.')
    parser.add_argument('name', nargs='?', default='Chuck Norris', help='Use another name.')
    parser.add_argument('--number', '-n', type=int, dest='quip_number', help='Pick a specific quip.')

    return parser.parse_args()

def main():
    args = parse_args()

    print(quip(name=args.name, number=args.quip_number))