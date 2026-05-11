import sqlite3
import urllib.request
from urllib.error import HTTPError
import os

from berea.utils import get_app_data_path


def clean_book_name(book):
        cleaned_name = book.title()
        # Database names use proper title case
        # eg. 'Song of Solomon' and 'Revelation of John'
        if 'Of' in cleaned_name:
            cleaned_name = cleaned_name.replace('Of', 'of')
        return cleaned_name


def parse_verses_str(verses):
    verses_split = verses.split('-')
    return verses_split[0], verses_split[1]


def list_to_sql(data):
    return "('" + "','".join(data) + "')"


class BibleInputError(ValueError):
    pass


class BibleClient:
    def __init__(self, translation):
        self.translation = translation
        # Use venv path or platform app data path to store translation DBs
        self.database = f"{get_app_data_path('translations')}/{self.translation}.db"
    
    def download_raw_bible(self):
        url = f"https://github.com/jstadnik619/bible_databases/raw/refs/heads/master/formats/sqlite/{self.translation}.db"

        try:
            urllib.request.urlretrieve(url, self.database)
            return f"Downloaded: {self.database}"
            
        except HTTPError:
            link = "https://github.com/jstadnik619/bible_databases?tab=readme-ov-file#available-translations-140"
            msg = (
                f"Translation '{self.translation}' does not exist.\n"
                f"Check the following link for available translations:\n{link}"
            )
            raise BibleInputError(msg)
    
    # TODO: Close out the conn when it's released
    def get_bible_cursor(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        # TODO: Use context manager?
        return conn.cursor()
    
    def delete_translation(self):
        os.remove(self.database)
        return f"Deleted translation '{self.translation}'."
    
    def get_book_abbreviation_by_resource(self, book, resource):
        """Get a book's abbreviation used by a specific resource.
        """
        cursor = self.get_bible_cursor()
   
        params = {
            'book': book,
            'resource': resource,
        }
        
        cursor.execute("""
            SELECT abbreviation FROM abbreviations
            JOIN books ON abbreviations.book_id = books.id
            JOIN resources_abbreviations ON resources_abbreviations.abbreviation_id = abbreviations.id
            JOIN resources ON resources_abbreviations.resource_id = resources.id
            WHERE books.name = :book
            AND resources.name = :resource
            """, params)
        
        # Assuming a resource only has one abbreviation for a given book and translation
        # STEP Bible abbreviations are in title case
        return cursor.fetchone()[0].title()
    
    def get_book_from_abbreviation(self, book):
        cleaned_book_name = clean_book_name(book)
        cursor = self.get_bible_cursor()
        
        # Use full book name if that was passed in
        book_row = cursor.execute(
            """SELECT * FROM books WHERE books.name = ?;""",
            (cleaned_book_name,)).fetchone()
        
        if book_row:
            return cleaned_book_name
        
        # Get full book name using abbreviation
        else:
            book_row = cursor.execute("""
            SELECT * FROM books
            JOIN abbreviations ON abbreviations.book_id = books.id
            WHERE abbreviations.abbreviation = ?;
            """, (book,)).fetchone()
            
            if book_row:
                return book_row['name']
            else:
                raise BibleInputError(f"Invalid input {book=}.")
    
    # TODO: Link format depends on resource
    def create_link(self, book, chapter=None, verse=None, resource='STEP Bible'):
        book_abbrev = self.get_book_abbreviation_by_resource(book, resource)
        
        link = ''
        
        if verse:
            # Parse verses if multiple provided
            if '-' in verse:
                verse_start, verse_end = parse_verses_str(verse)
                link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}.{chapter}.{verse_start}-{book_abbrev}.{chapter}.{verse_end}&options=NVHUG"
                
            else:
                link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}.{chapter}.{verse}&options=NVHUG"
        
        elif chapter:
            link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}.{chapter}&options=NVHUG"
        
        # Make link for whole book
        else:
            link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}&options=NVHUG"

        return link

    def get_verses_by_book(self, book):
        cursor = self.get_bible_cursor()
        book = self.get_book_from_abbreviation(book)
        params = {'book': book}
    
        cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        """, params)

        verse_records = cursor.fetchall()
        
        return verse_records

    # TODO: Validate chapter?
    def get_verses_by_chapter(self, book, chapter):
        cursor = self.get_bible_cursor()
        book = self.get_book_from_abbreviation(book)
        params = {'book': book, 'chapter': chapter}
        
        cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        """, params)

        verse_records = cursor.fetchall()
        
        if len(verse_records) == 0:
            raise BibleInputError(f"Invalid chapter: {book} {chapter}.")
        
        else:
            return verse_records

    # TODO: Validate chapter?
    def get_verse(self, book, chapter, verse):
        cursor = self.get_bible_cursor()
        book = self.get_book_from_abbreviation(book)
        params = {
            'book': book,
            'chapter': chapter,
            'verse': verse
        }
        
        cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        AND verse = :verse
        """, params)

        verse_records = cursor.fetchall()
        
        if len(verse_records) == 0:
            raise BibleInputError(f"Invalid verse: {book} {chapter}:{verse}.")
        
        else:
            return verse_records

    # TODO: Validate chapter?
    # def get_verses(self, book, chapter, verse):
    #     """
    #     Print a range of verses, eg. 5-7. 
    #     """
    #     cursor = self.get_bible_cursor()
    #     book = self.get_book_from_abbreviation(book)
    #     verse_start, verse_end = parse_verses_str(verse)
        
    #     params = {
    #         'book': book,
    #         'chapter': chapter,
    #         'verse_start': verse_start,
    #         'verse_end': verse_end,
    #     }
        
    #     cursor.execute("""
    #     SELECT verse, text FROM verses
    #     JOIN books ON verses.book_id = books.id
    #     WHERE books.name = :book
    #     AND chapter = :chapter
    #     AND verse BETWEEN :verse_start AND :verse_end
    #     """, params)

    #     verse_records = cursor.fetchall()
        
    #     if len(verse_records) == 0:
    #         raise BibleInputError(
    #             f"Invalid verses: {book} "
    #             f"{chapter}:{verse_start}-{verse_end}."
    #         )
        
    #     else:
    #         return verse_records
    
    def get_markup_by_book():
        pass
    
    def get_markup_by_chapter(self, book, chapter):
        cursor = self.get_bible_cursor()
        book = self.get_book_from_abbreviation(book)
        params = {'book': book, 'chapter': chapter}
        
        cursor.execute("""
        SELECT verse, text, marker FROM markup
        JOIN books ON markup.book_id = books.id
        WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
        AND books.name = :book
        AND chapter = :chapter
        """, params)

        markup_records = cursor.fetchall()
        
        if len(markup_records) == 0:
            raise BibleInputError(f"Invalid chapter: {book} {chapter}.")
        
        else:
            return markup_records
    
    def get_markup_for_verse(self, book, chapter, verse):
        """
        Print a range of verses, eg. 5-7. 
        """
        cursor = self.get_bible_cursor()
        book = self.get_book_from_abbreviation(book)
        
        params = {
            'book': book,
            'chapter': chapter,
            'verse': verse,
        }
        
        cursor.execute("""
        SELECT verse, text, marker FROM markup
        JOIN books ON markup.book_id = books.id
        WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
        AND books.name = :book
        AND chapter = :chapter
        AND verse = :verse;
        """, params)

        markup_records = cursor.fetchall()
        
        if len(markup_records) == 0:
            raise BibleInputError(f"Invalid verse: {book} {chapter}:{verse}.")
        
        else:
            return markup_records

    def get_markup_for_verses(self, book, chapter, verse):
        """
        Print a range of verses, eg. 5-7. 
        """
        cursor = self.get_bible_cursor()
        book = self.get_book_from_abbreviation(book)
        verse_start, verse_end = parse_verses_str(verse)
        
        params = {
            'book': book,
            'chapter': chapter,
            'verse_start': verse_start,
            'verse_end': verse_end,
        }
        
        cursor.execute("""
        SELECT verse, text, marker FROM markup
        JOIN books ON markup.book_id = books.id
        WHERE marker IN ('b', 'm', 'pmo', 'li1', 'q1', 'q2')
        AND books.name = :book
        AND chapter = :chapter
        AND verse BETWEEN :verse_start AND :verse_end;
        """, params)

        markup_records = cursor.fetchall()
        
        if len(markup_records) == 0:
            raise BibleInputError(
                f"Invalid verses: {book} "
                f"{chapter}:{verse_start}-{verse_end}."
            )
        
        else:
            return markup_records

    def search_bible(self, phrase):
        cursor = self.get_bible_cursor()
        
        # TODO: Order by rank?
        cursor.execute("""
        SELECT
            books.name AS book,
            chapter,
            verse,
            highlight(fts_verses, 3, '<b>', '</b>') AS text
        FROM fts_verses
        JOIN books ON fts_verses.book_id = books.id
        WHERE fts_verses MATCH ?;
        """, (phrase,))
        
        return cursor.fetchall()
    
    def search_testament(self, phrase, testament):
        cursor = self.get_bible_cursor()
        
        new_testament = [
            'Matthew',
            'Mark',
            'Luke',
            'John',
            'Acts',
            'Romans',
            'I Corinthians',
            'II Corinthians',
            'Galatians',
            'Ephesians',
            'Philippians',
            'Colossians',
            'I Thessalonians',
            'II Thessalonians',
            'I Timothy',
            'II Timothy',
            'Titus',
            'Philemon',
            'Hebrews',
            'James',
            'I Peter',
            'II Peter',
            'I John',
            'II John',
            'III John',
            'Jude',
            'Revelation of John'
        ]

        nt_sql_list = list_to_sql(new_testament)

        if testament == 'nt':
            sql = f"""
            SELECT
                books.name AS book,
                chapter,
                verse,
                highlight(fts_verses, 3, '<b>', '</b>') AS text
            FROM fts_verses
            JOIN books ON fts_verses.book_id = books.id
            WHERE fts_verses MATCH ?
            AND books.name IN {nt_sql_list};
            """
        
        elif testament == 'ot': 
            sql = f"""
            SELECT
                books.name AS book,
                chapter,
                verse,
                highlight(fts_verses, 3, '<b>', '</b>') AS text
            FROM fts_verses
            JOIN books ON fts_verses.book_id = books.id
            WHERE fts_verses MATCH ?
            AND books.name NOT IN {nt_sql_list};
            """
        
        else:
            raise BibleInputError(f"Invalid {testament=}.")
        
        # Bind phrase since it's user input
        cursor.execute(sql, (phrase,))
        return cursor.fetchall()
    
    def search_book(self, phrase, book):
        cursor = self.get_bible_cursor()

        book = self.get_book_from_abbreviation(book)
        params = {
            'phrase': phrase,
            'book': book
        }
        
        cursor.execute("""
        SELECT
            books.name AS book,
            chapter,
            verse,
            highlight(fts_verses, 3, '<b>', '</b>') AS text
        FROM fts_verses
        JOIN books ON fts_verses.book_id = books.id
        WHERE fts_verses MATCH :phrase
        AND book = :book;
        """, params)

        
        return cursor.fetchall()

    # TODO: Validate chapter?
    def search_chapter(self, phrase, book, chapter):
        cursor = self.get_bible_cursor()

        book = self.get_book_from_abbreviation(book)
        params = {
            'phrase': phrase,
            'book': book,
            # FTS will fail if chapter is passed as a string
            'chapter': int(chapter),
        }
        
        cursor.execute("""
        SELECT
            books.name AS book,
            chapter,
            verse,
            highlight(fts_verses, 3, '<b>', '</b>') AS text
        FROM fts_verses
        JOIN books ON fts_verses.book_id = books.id
        WHERE fts_verses MATCH :phrase
        AND book = :book
        AND chapter = :chapter;
        """, params)
        
        return cursor.fetchall()
