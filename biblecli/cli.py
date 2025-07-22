import sys
import os
import configparser
import argparse
# BUG: ImportError: cannot import name '__version__' from 'biblecli' (unknown location)
# from biblecli import __version__
from biblecli.utils import get_downloaded_translations
from biblecli.bible import BibleClient


# TODO: Remove this
def get_config_path():
    system_platform = sys.platform
    
    # Check if a virtual environment is active
    # BUG: This doesn't work if biblecli is also installed globally?
    if hasattr(sys, 'prefix') and sys.prefix != sys.base_prefix:
        # Set path to the root of the venv
        venv_root = sys.prefix
        
        if system_platform == 'win32':
            return os.path.join(venv_root, 'biblecli.ini')
        else:  # Linux, macOS
            return os.path.join(venv_root, 'biblecli.conf')
    
    # No venv, use OS's standard path for config
    else:
        if system_platform == 'win32':
            return os.path.join(os.environ.get('APPDATA', ''), 'biblecli', 'biblecli.ini')
        elif system_platform == 'darwin':  # macOS
            # TODO: Create biblecli directory if it doesn't exist?
            return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'biblecli', 'biblecli.conf')
        elif system_platform == 'linux':
            return os.path.join(os.path.expanduser('~'), '.config', 'biblecli', 'biblecli.conf')
        
        else:
            sys.exit(f"Unsupported platform: {system_platform}")


class CLIConfig:
    config = configparser.ConfigParser()
    # TODO: Use get_app_data_path() instead
    path = get_config_path()
    
    @classmethod
    def set_default_translation(cls, translation):
        if not cls.config.has_section('Defaults'):
            cls.config.add_section('Defaults')
        
        cls.config.set('Defaults', 'translation', translation)
        
        # BUG: This raises FileNotFoundError: [Errno 2] No such file or directory: '/Users/jamiestadnik/Library/Application Support/biblecli/biblecli.conf'
        with open(cls.path, 'w') as config_file:
            cls.config.write(config_file)
    
    @classmethod
    def get_default_translation(cls):
        cls.config.read(cls.path)
        return cls.config.get('Defaults', 'translation', fallback=None)


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
    
    
def add_delete_parser(subparsers, downloaded_translations):
    delete_parser = subparsers.add_parser(
        'delete',
        help="Delete a Bible translation"
    )
    
    delete_parser.add_argument(
        'translation',
        choices=downloaded_translations
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

    search_parser.add_argument(
        'book',
        nargs='?'
    )

    search_parser.add_argument('chapter', nargs='?')
    search_parser.add_argument('verse', nargs='?')
    
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


def parse_biblecli_args(downloaded_translations):
    description = "A CLI for looking up passages of Scripture."
    parser = argparse.ArgumentParser(description=description)
    # parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--version', action='version', version=f'%(prog)s 0.0.1')  # TODO: use __version__
    
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    add_reference_parser(subparsers, downloaded_translations)
    add_download_parser(subparsers)
    add_delete_parser(subparsers, downloaded_translations)
    add_search_parser(subparsers, downloaded_translations)
    add_config_parser(subparsers, downloaded_translations)
    
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
        'config',
        '--version',
        '--help',
        '-h',
    ]
    
    if sys.argv[1] not in commands:
        sys.argv.insert(1, 'reference')
    
    downloaded_translations = get_downloaded_translations()
    args = parse_biblecli_args(downloaded_translations)

    if args.command == 'config':
        CLIConfig.set_default_translation(args.value)
        print('Default translation updated.')
        return 

    bible = BibleClient(args.translation)
    
    match args.command:
        case 'download':
            # Save first downloaded translation as the default
            if not downloaded_translations:
                CLIConfig.set_default_translation(args.translation)
            
            bible.create_bible_db()
        
        case 'delete':
            bible.delete_translation()

            # Update config if no other translation is downloaded
            if [args.translation] == downloaded_translations:
                CLIConfig.set_default_translation('None')
            
            # Update config if default translation is deleted
            if args.translation == CLIConfig.get_default_translation():
                CLIConfig.set_default_translation(downloaded_translations[0])
    
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
