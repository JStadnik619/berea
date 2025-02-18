import sqlite3

conn = sqlite3.connect('KJV.db')


cursor = conn.cursor()

cursor.execute("""
SELECT text FROM KJV_verses
WHERE book_id = 8
AND chapter = 4
AND verse = 1
""")

records = cursor.fetchall()
for row in records:
    print(row)
