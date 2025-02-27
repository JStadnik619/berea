import sqlite3
import os
import json


def get_source_root():
    return os.path.realpath(os.path.dirname(__file__))


# TODO: Run this when downloading new translation from the CLI
def rename_tables(translation):
    """Rename tables for consistent schema across downloaded translations.
    """
    database = f'{get_source_root()}/data/{translation}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    tables = ['books', 'verses']
    for table in tables:
        # SQLite doesn't bind parameters for schema objects
        sql = f"ALTER TABLE {translation}_{table} RENAME TO {table};"
        cursor.execute(sql)


# TODO: Add abbreviations and short names to books table, add to returned list
def valid_books(translation):
    database = f'{get_source_root()}/data/{translation}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM books")

    records = cursor.fetchall()
    
    books = []
    
    for row in records:
        books.append(row[0])
        
    return books


def clean_book_name(book):
    cleaned_name = book.title()
    # Database names use proper title case
    # eg. 'Song of Solomon' and 'Revelation of John'
    if 'Of' in cleaned_name:
        cleaned_name = cleaned_name.replace('Of', 'of')
    return cleaned_name


# TODO: Create a table for these mappings in the db upon download
def get_book_from_abbreviation(book):
    books_to_abbreviations = {}
    with open(f'{get_source_root()}/data/book_abbreviations.json') as file:
        books_to_abbreviations = dict(json.load(file))
    
    cleaned_book_name = clean_book_name(book)
        
    if cleaned_book_name in books_to_abbreviations.keys():
        return cleaned_book_name
    
    else:
        for book_name, abbreviations in books_to_abbreviations.items():
            if book.lower() in abbreviations:
                return book_name
        
        msg = f"Invalid input {book=}."
        print(msg)


def create_empty_markdown_link(params):
    """Creates an empty link since mapping a book's abbreviation to
    a URL path variable would be overly complex.
    """
    link = f"([{params['book']}"
    
    if params['chapter']:
        link += f" {params['chapter']}"
        
        if params['verse']:
            link += f":{params['verse']}"
    
    link += f" {params['translation']}]())"
    
    return link


def list_multiline_verse(verse):
    lines = []
    
    next_line = verse
    
    while len(next_line) > 80:
        # Split the verse if there's more than one line left
        space_split = next_line[:79].rfind(' ')
        lines.append(next_line[:space_split])
        next_line = next_line[space_split:].lstrip()
            
    # Append last line of verse
    lines.append(next_line)
    
    return lines


# TODO: Adjustable line length? (BSB wraps lines at 40-43 characters)
def print_single_or_multiline_verse(verse_record):
    # Print single line verse
    if len(verse_record[0]) <= 80:
        print(verse_record[0])
    
    # Split the verse into multiple lines if it's too long
    else:
        lines = list_multiline_verse(verse_record[0])
        for line in lines:
            print(line)


# TODO: Replace consecutive spaces with single spaces
# TODO: Input line length?
def print_wall_of_text(verse_records, verse_numbers=False): 
    verses = ''
    for row in verse_records:
        if verse_numbers:
            verses += str(row['verse']) + ' '
        
        verses += row['text'].strip() + ' '
    
    verses_split = list_multiline_verse(verses)
    wrapped_verses = '\n'.join(verses_split)
    
    print(wrapped_verses)


# TODO: Print paragraphs from Bible format
def print_markdown_excerpt(verse_records, params):
    """Generate Markdown excerpt for the verses.

    Args:
        verse_records (_type_): _description_
        params (_type_): _description_
    """
    print('###\n')
    print('______________________________________________________________________\n')
    print_wall_of_text(verse_records)
    print(create_empty_markdown_link(params))
    print('\n______________________________________________________________________')


# TODO: Print paragraphs from Bible format
# TODO: Parse USFM tags to create more readable passages/newlines
def print_passage_by_format(params, verse_records):
    match params['format']: 
        case 'txt':
            print_wall_of_text(verse_records, params['verse_numbers'])

        case 'md':
            print_markdown_excerpt(verse_records, params)


def get_bible_cursor(translation):
    database = f"{get_source_root()}/data/{translation}.db"
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    # TODO: Use context manager?
    return conn.cursor()


def print_book(params):
    cursor = get_bible_cursor(params['translation'])
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        """, params)

        verse_records = cursor.fetchall()
        
        print_passage_by_format(params, verse_records)


def print_chapter(params):
    cursor = get_bible_cursor(params['translation'])
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        """, params)

        verse_records = cursor.fetchall()
        
        if len(verse_records) == 0:
            msg = f"Invalid chapter: {params['book']} {params['chapter']}"
            print(msg)
        
        else:
            print_passage_by_format(params, verse_records)


def print_verse(params):
    cursor = get_bible_cursor(params['translation'])
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        AND verse = :verse
        """, params)

        verse_records = cursor.fetchall()
        
        if len(verse_records) == 0:
            msg = f"Invalid verse: {params['book']} {params['chapter']}:{params['verse']}"
            print(msg)
        
        else:
            print_passage_by_format(params, verse_records)


def print_verses(params):
    """
    Print a range of verses, eg. 5-7. 
    """
    cursor = get_bible_cursor(params['translation'])
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        verses = params['verse'].split('-')
        params['verse_start'] = verses[0]
        params['verse_end'] = verses[1]
        
        cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        AND verse BETWEEN :verse_start AND :verse_end
        """, params)

        verse_records = cursor.fetchall()
        
        if len(verse_records) == 0:
            msg = (
                f"Invalid verses: {params['book']} "
                f"{params['chapter']}:{params['verse_start']}-{params['verse_end']}"
            )
            print(msg)
        
        else:
            print_passage_by_format(params, verse_records)
    
    
    # TODO: Use FTS4 SQLite extension to search bible for particular words/phrases
    # TODO: Fuzzy search? (eg. sanctify, sanctification, sanctity)
    def search_bible():
        pass
