import argparse

from biblecli import __version__
from biblecli.bible import BibleClient


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
        choices=['BSB', 'KJV'],
        default='BSB'
    )
    
    # TODO: Make the default format configurable
    parser.add_argument(
        '-f', '--format',
        choices=['txt', 'md'],
        default='txt'
    )
    parser.add_argument(
        '-n', '--verse_numbers',
        action='store_true'
    )
    
    return parser.parse_args()


def main():
    args = parse_biblecli_args()
    
    if args is not None:
        params = vars(args)
        
        bible = BibleClient(**params)

        if not args.chapter:
            bible.print_book()
        elif not args.verse:
           bible.print_chapter()
        elif '-' in args.verse:
            bible.print_verses()
        else:
           bible.print_verse()


if __name__ == "__main__":
    main()
