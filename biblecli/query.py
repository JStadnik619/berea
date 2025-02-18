import sqlite3
import os


def get_source_root():
    return os.path.realpath(os.path.dirname(__file__))


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
