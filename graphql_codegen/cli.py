"""CLI utility for graphql-codegen."""
from argparse import ArgumentParser


def main() -> None:
    """Entry point for the cli utility."""
    parser = ArgumentParser()
    parser.add_argument(
        'sources',
        nargs='+',
        type=str,
        help='Source of queries & mutation documents',
        metavar='SOURCE_LIST'
    )
