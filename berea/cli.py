import sys
import configparser
import argparse
from berea.utils import get_downloaded_translations, get_app_data_path
from berea.bible import BibleClient, BibleInputError
from berea.render import render_reference_results, render_search_results


# Version stored here to prevent editable install ImportError
__version__ = '0.1.1'


class CLIConfig:
    config = configparser.ConfigParser()
    path = get_app_data_path() + '/berea.ini'
    
    @classmethod
    def set_default_translation(cls, translation):
        if not cls.config.has_section('Defaults'):
            cls.config.add_section('Defaults')
        
        cls.config.set('Defaults', 'translation', translation)
        
        with open(cls.path, 'w') as config_file:
            cls.config.write(config_file)
    
    @classmethod
    def get_default_translation(cls):
        cls.config.read(cls.path)
        return cls.config.get('Defaults', 'translation', fallback=None)


def add_download_parser(subparsers):
    download_parser = subparsers.add_parser(
        'download',
        help="Download a Bible translation"
    )
    
    download_parser.add_argument(
        'translation',
        default='KJV'
    )
    
    
def add_delete_parser(subparsers, downloaded_translations):
    delete_parser = subparsers.add_parser(
        'delete',
        help="Delete a Bible translation"
    )
    
    delete_parser.add_argument(
        'translation',
        choices=downloaded_translations
    )


def add_config_parser(subparsers, downloaded_translations):
    config_parser = subparsers.add_parser(
        'config',
        help="Configure default settings"
    )

    config_parser.add_argument(
        'parameter',
        choices=['translation']
    )

    config_parser.add_argument(
        'value',
        choices=downloaded_translations
    )


def add_reference_parser(subparsers, downloaded_translations):
    reference_parser = subparsers.add_parser(
        'reference',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Reference a passage from the Bible (default command)"
    )
    
    reference_parser.add_argument(
        'book'
    )

    reference_parser.add_argument('chapter', nargs='?')
    reference_parser.add_argument('verse', nargs='?')
    
    reference_parser.add_argument(
        '-t', '--translation',
        choices=downloaded_translations,
        default=CLIConfig.get_default_translation(),
        help='Bible translation used to display passage'
    )
    
    reference_parser.add_argument(
        '-n', '--verse_numbers',
        action='store_true'
    )
    
    # TODO: Make the default format configurable
    reference_parser.add_argument(
        '-f', '--format',
        choices=['txt', 'md'],
        default='txt'
    )
    
    
def add_search_parser(subparsers, downloaded_translations):
    search_parser = subparsers.add_parser(
        'search',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Search for a specific phrase in a Bible translation"
    )
    
    search_parser.add_argument(
        'phrase',
        help="Phrase to search"
    )
    
    search_parser.add_argument('book', nargs='?')
    search_parser.add_argument('chapter', nargs='?')
    
    search_parser.add_argument(
        '-t', '--translation',
        choices=downloaded_translations,
        default=CLIConfig.get_default_translation(),
        help='Bible translation used to search phrase'
    )

    search_parser.add_argument(
        '-NT', '--new_testament',
        action='store_true'
    )

    search_parser.add_argument(
        '-OT', '--old_testament',
        action='store_true'
    )


def parse_berea_args(downloaded_translations):
    description = "Berea: A CLI for studying Scripture."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    add_download_parser(subparsers)
    add_delete_parser(subparsers, downloaded_translations)
    add_config_parser(subparsers, downloaded_translations)
    add_reference_parser(subparsers, downloaded_translations)
    add_search_parser(subparsers, downloaded_translations)
    
    return parser.parse_args()


def main():
    if len(sys.argv) < 2:
        sys.argv = ['bible', '--help']
    
    commands = [
        '--help',
        '-h',
        '--version',
        'download',
        'delete',
        'config',
        'reference',
        'search',
    ]
    
    # Set reference as the default command
    if sys.argv[1] not in commands:
        sys.argv.insert(1, 'reference')
    
    downloaded_translations = get_downloaded_translations()
    args = parse_berea_args(downloaded_translations)

    if args.command == 'config':
        CLIConfig.set_default_translation(args.value)
        print('Default translation updated.')
        return 

    bible = BibleClient(args.translation)
    output = ''
    
    if args.command == 'download':
        # Save first downloaded translation as the default
        if not downloaded_translations:
            CLIConfig.set_default_translation(args.translation)
        
        try:
            output = bible.create_bible_db()
        except BibleInputError as ex:
            output = str(ex)
    
    elif not downloaded_translations:
        output = f"Error: Download a translation before invoking '{args.command}'."
        
    elif args.command == 'delete':
        output = bible.delete_translation()

        # Update config if no other translation is downloaded
        if [args.translation] == downloaded_translations:
            CLIConfig.set_default_translation('None')
        
        # Update config if default translation is deleted
        if args.translation == CLIConfig.get_default_translation():
            CLIConfig.set_default_translation(get_downloaded_translations()[0])

    elif args.command ==  'reference':
        verse_records = []
        
        try:
            if not args.chapter:
                verse_records = bible.get_verses_by_book(args.book)
            elif not args.verse:
                verse_records = bible.get_verses_by_chapter(
                    args.book,
                    args.chapter
                )
            elif '-' in args.verse:
                verse_records = bible.get_verses(
                    args.book,
                    args.chapter,
                    args.verse
                )
            else:
                verse_records = bible.get_verse(
                    args.book,
                    args.chapter,
                    args.verse
                )
            
            output = render_reference_results(
                bible,
                args.format,
                verse_records,
                args.verse_numbers,
                args.book,
                args.chapter,
                args.verse
            )
        except BibleInputError as ex:
            output = str(ex)
        
    elif args.command ==  'search':
        verse_records = []
        if args.chapter:
            if args.new_testament:
                output = (
                    "Invalid search: cannot search a chapter with the "
                    "'-NT, --new_testament' flag."
                )
            elif args.old_testament:
                output = (
                    "Invalid search: cannot search a chapter with the "
                    "'-OT, --old_testament' flag."
                )
            else:
                verse_records = bible.search_chapter(args.phrase, args.book, args.chapter)
        elif args.book:
            if args.new_testament:
                output = (
                    "Invalid search: cannot search a book with the "
                    "'-NT, --new_testament' flag."
                )
            elif args.old_testament:
                output = (
                    "Invalid search: cannot search a book with the "
                    "'-OT, --old_testament' flag."
                )
            else:
                verse_records = bible.search_book(args.phrase, args.book)
        elif args.new_testament:
            verse_records = bible.search_testament(args.phrase , 'nt')
        elif args.old_testament:
            verse_records = bible.search_testament(args.phrase , 'ot')
        else:
            verse_records = bible.search_bible(args.phrase)
        
        testament = None
        if args.new_testament:
            testament = 'nt'
        elif args.old_testament:
            testament = 'ot'
        
        if verse_records:
            output = render_search_results(
                bible,
                verse_records,
                args.phrase,
                testament,
                args.book,
                args.chapter
            )
    
    print(output)


if __name__ == "__main__":
    main()
