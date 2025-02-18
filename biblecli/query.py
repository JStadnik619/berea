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


def print_verse(params, version='KJV'):
    database = f'{get_source_root()}/data/{version}.db'
    conn = sqlite3.connect(database)
    # TODO: Use context manager?
    cursor = conn.cursor()
    
    # TODO: Pass version as query param
    
    # TODO: Parse verse if in format eg. 5-7 
    
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
