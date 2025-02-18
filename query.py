import sqlite3


def print_verse(conn, params):
    # TODO: Use context manager?
    cursor = conn.cursor()
    cursor.execute("""
    SELECT text FROM KJV_verses
    JOIN KJV_books ON KJV_verses.book_id = KJV_books.id
    WHERE KJV_books.name = :book
    AND chapter = :chapter
    AND verse = :verse
    """, params)

    records = cursor.fetchall()
    for row in records:
        print(row)


# TODO: Remove this once cli.py and entry point implemented
if __name__ == '__main__':
    conn = sqlite3.connect('KJV.db')
    params = {'book': 'Genesis', 'chapter': 3, 'verse': 3}
    print_verse(conn, params)