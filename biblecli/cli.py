import argparse

from biblecli import __version__
from biblecli.query import (
    print_verse, valid_books, print_book, print_chapter, print_verses
)


# Example: python -m biblecli.cli Genesis 3 3
def parse_biblecli_args():
    description = "A CLI for looking up passages of Scripture."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    # TODO: Improve message returned by invalid choice
    # TODO: eg. fuzzy match input to valid name/abbr
    parser.add_argument(
        'book'#,
        # TODO: Uncomment this once abbreviations are returned by valid_books()
        # choices=valid_books()
    )

    parser.add_argument('chapter', nargs='?')
    parser.add_argument('verse', nargs='?')
    
    parser.add_argument(
        '-t', '--translation',
        # TODO: parse choices from /data
        choices=['KJV', 'BSB'],
        default='KJV'
    )
    
    # TODO: Make the default format configurable
    parser.add_argument(
        '-f', '--format',
        choices=['txt', 'md'],
        default='txt'
    )
    
    return parser.parse_args()


# TODO: markdown output format
def main():
    args = parse_biblecli_args()
    
    if args is not None:
        params = vars(args)

        if not args.chapter:
            print_book(params)
        elif not args.verse:
            print_chapter(params)
        elif '-' in args.verse:
            print_verses(params)
        else:
            print_verse(params)


if __name__ == "__main__":
    main()
