import sqlite3

conn = sqlite3.connect('KJV.db')


cursor = conn.cursor()

cursor.execute("""
SELECT text FROM KJV_verses
JOIN KJV_books ON KJV_verses.book_id = KJV_books.id
WHERE KJV_books.name = 'Genesis'
AND chapter = 4
AND verse = 1
""")

records = cursor.fetchall()
for row in records:
    print(row)
