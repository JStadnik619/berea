import sys
import argparse

from biblecli import __version__
from biblecli.utils import get_downloaded_translations
from biblecli.bible import BibleClient


DOWNLOADED_TRANSLATIONS = get_downloaded_translations()


def add_reference_parser(subparsers):
    reference_parser = subparsers.add_parser(
        'reference',
        help="Reference a passage from the Bible (default command)"
    )
    
    reference_parser.add_argument(
        'book'
    )

    reference_parser.add_argument('chapter', nargs='?')
    reference_parser.add_argument('verse', nargs='?')
    
    # TODO: Make the default translation configurable
    reference_parser.add_argument(
        '-t', '--translation',
        # TODO: parse choices from /data/db
        choices=DOWNLOADED_TRANSLATIONS,
        default='BSB'
    )
    
    # TODO: Make the default format configurable
    reference_parser.add_argument(
        '-f', '--format',
        choices=['txt', 'md'],
        default='txt'
    )
    reference_parser.add_argument(
        '-n', '--verse_numbers',
        action='store_true'
    )


def add_download_parser(subparsers):
    download_parser = subparsers.add_parser(
        'download',
        help="Download a bible translation"
    )
    
    download_parser.add_argument(
        'translation',
        # choices=[],
        default='KJV'
    )


def parse_biblecli_args():
    description = "A CLI for looking up passages of Scripture."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    add_reference_parser(subparsers)
    add_download_parser(subparsers)
    
    return parser.parse_args()


def main():
    # Set reference as the default command
    if sys.argv[1] not in ['reference', 'download', '--help', '-h']:
        sys.argv.insert(1, 'reference')
    
    args = parse_biblecli_args()
    
    if args is not None:

        bible = BibleClient(args.translation)
        command = args.command
        
        if command == 'download':
            bible.create_bible_db()
        
        else:

            if not args.chapter:
                bible.print_book(args.book, args.format, args.verse_numbers)
            elif not args.verse:
                bible.print_chapter(
                    args.book,
                    args.chapter,
                    args.format,
                    args.verse_numbers
                    )
            elif '-' in args.verse:
                bible.print_verses(
                    args.book,
                    args.chapter,
                    args.verse,
                    args.format,
                    args.verse_numbers
                )
            else:
                bible.print_verse(
                    args.book,
                    args.chapter,
                    args.verse,
                    args.format,
                    args.verse_numbers
                    )


if __name__ == "__main__":
    main()
