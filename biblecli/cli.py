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
        help="Download a Bible translation"
    )
    
    download_parser.add_argument(
        'translation',
        default='KJV'
    )
    
    
def add_delete_parser(subparsers):
    delete_parser = subparsers.add_parser(
        'delete',
        help="Delete a Bible translation"
    )
    
    delete_parser.add_argument(
        'translation',
        choices=DOWNLOADED_TRANSLATIONS
    )
    
    
def add_search_parser(subparsers):
    search_parser = subparsers.add_parser(
        'search',
        help="Search for a specific phrase in a Bible translation"
    )
    
    search_parser.add_argument(
        'phrase',
        help="Phrase to search"
    )

    search_parser.add_argument(
        'book',
        nargs='?'
    )

    search_parser.add_argument('chapter', nargs='?')
    search_parser.add_argument('verse', nargs='?')
    
    search_parser.add_argument(
        '-t', '--translation',
        choices=DOWNLOADED_TRANSLATIONS,
        default='BSB'
    )

    search_parser.add_argument(
        '-NT', '--new_testament',
        action='store_true'
    )

    search_parser.add_argument(
        '-OT', '--old_testament',
        action='store_true'
    )


def parse_biblecli_args():
    description = "A CLI for looking up passages of Scripture."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    add_reference_parser(subparsers)
    add_download_parser(subparsers)
    add_delete_parser(subparsers)
    add_search_parser(subparsers)
    
    return parser.parse_args()


def main():
    if len(sys.argv) < 2:
        sys.argv = ['bible', '--help']
    
    # Set reference as the default command
    commands = [
        'reference',
        'download',
        'delete',
        'search',
        '--help',
        '-h',
    ]
    
    if sys.argv[1] not in commands:
        sys.argv.insert(1, 'reference')
    
    args = parse_biblecli_args()
    
    bible = BibleClient(args.translation)
    
    match args.command:
        case 'download':
            bible.create_bible_db()
        
        case 'delete':
            bible.delete_translation()
    
        case 'reference': 
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
            
        case 'search':
            if args.chapter:
                bible.search_chapter(args.phrase, args.book, args.chapter)
            elif args.book:
                bible.search_book(args.phrase, args.book)
            elif args.new_testament:
                bible.search_testament(args.phrase , 'nt')
            elif args.old_testament:
                bible.search_testament(args.phrase , 'ot')
            else:
                bible.search_bible(args.phrase)


if __name__ == "__main__":
    main()
