import sqlite3
import os
import json


def get_source_root():
    return os.path.realpath(os.path.dirname(__file__))


# TODO: Add abbreviations and short names to books table, add to returned list
def valid_books(version='KJV'):
    database = f'{get_source_root()}/data/{version}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    # TODO: Pass version as query param
    cursor.execute("SELECT name FROM KJV_books")

    records = cursor.fetchall()
    
    books = []
    
    for row in records:
        books.append(row[0])
        
    return books


# TODO: print_book

# TODO: print_chapter


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


def print_verse(params, version='KJV'):
    database = f'{get_source_root()}/data/{version}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    # TODO: Pass version as query param
    
    if params['book']:
    
        cursor.execute("""
        SELECT text FROM KJV_verses
        JOIN KJV_books ON KJV_verses.book_id = KJV_books.id
        WHERE KJV_books.name = :book
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


def print_verses(params, version='KJV'):
    """
    Print a range of verses, eg. 5-7. 
    """
    database = f'{get_source_root()}/data/{version}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = get_book_from_abbreviation(params['book'])
    
    if params['book']:
    
        verses = params.pop('verse').split('-')
        params['verse_start'] = verses[0]
        params['verse_end'] = verses[1]
        
        # TODO: Pass version as query param
        
        cursor.execute("""
        SELECT text FROM KJV_verses
        JOIN KJV_books ON KJV_verses.book_id = KJV_books.id
        WHERE KJV_books.name = :book
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
