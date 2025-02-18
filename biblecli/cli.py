import argparse

from biblecli.query import print_verse, valid_books, print_verses


# Example: python -m biblecli.cli Genesis 3 3
def parse_biblecli_args():
    description = "A CLI for looking up passages of Scripture."
    parser = argparse.ArgumentParser(description=description)
    # parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    # TODO: Improve message returned by invalid choice
    parser.add_argument('book', choices=valid_books())
    # TODO: Parse chapter OR chapter:verse formats
    parser.add_argument('chapter')
    parser.add_argument('verse')
    
    return parser.parse_args()


def main():
    args = parse_biblecli_args()
    
    if args is not None:
        params = vars(args)
        if '-' in args.verse:
            print_verses(params)
        else:
            print_verse(params)


if __name__ == "__main__":
    main()