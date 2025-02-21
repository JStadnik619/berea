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


def print_book(params):
    database = f"{get_source_root()}/data/{params['translation']}.db"
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        cursor.execute("""
        SELECT text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        """, params)

        records = cursor.fetchall()
        
        for row in records:
                print(row[0])


def print_chapter(params):
    database = f"{get_source_root()}/data/{params['translation']}.db"
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        cursor.execute("""
        SELECT text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        """, params)

        records = cursor.fetchall()
        
        if len(records) == 0:
            msg = f"Invalid chapter: {params['book']} {params['chapter']}"
            print(msg)
        
        else:
            for row in records:
                print(row[0])


def print_verse(params):
    database = f"{get_source_root()}/data/{params['translation']}.db"
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        cursor.execute("""
        SELECT text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        AND verse = :verse
        """, params)

        records = cursor.fetchall()
        
        if len(records) == 0:
            msg = f"Invalid verse: {params['book']} {params['chapter']}:{params['verse']}"
            print(msg)
        
        else:
            for row in records:
                print(row[0])


def print_verses(params):
    """
    Print a range of verses, eg. 5-7. 
    """
    database = f"{get_source_root()}/data/{params['translation']}.db"
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        verses = params.pop('verse').split('-')
        params['verse_start'] = verses[0]
        params['verse_end'] = verses[1]
        
        cursor.execute("""
        SELECT text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        AND verse BETWEEN :verse_start AND :verse_end
        """, params)

        records = cursor.fetchall()
        
        if len(records) == 0:
            msg = (
                f"Invalid verses: {params['book']} "
                f"{params['chapter']}:{params['verse_start']}-{params['verse_end']}"
            )
            print(msg)
        
        else:
            for row in records:
                print(row[0])


# TODO: Generate Markdown reference to passage
