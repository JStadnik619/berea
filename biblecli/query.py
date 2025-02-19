import sqlite3
import os


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


# TODO: Filter book by abbreviations and short names (case-insensitive)
def print_verse(params, version='KJV'):
    database = f'{get_source_root()}/data/{version}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = clean_book_name(params['book'])
    
    # TODO: Pass version as query param
    
    cursor.execute("""
    SELECT text FROM KJV_verses
    JOIN KJV_books ON KJV_verses.book_id = KJV_books.id
    WHERE KJV_books.name = :book
    AND chapter = :chapter
    AND verse = :verse
    """, params)

    records = cursor.fetchall()
    for row in records:
        print(row[0])


# TODO: Filter book by abbreviations and short names (case-insensitive)
def print_verses(params, version='KJV'):
    """
    Print a range of verses, eg. 5-7. 
    """
    database = f'{get_source_root()}/data/{version}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    params['book'] = clean_book_name(params['book'])
    
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
    for row in records:
        print(row[0])


# TODO: Generate Markdown reference to passage
