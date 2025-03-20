import sqlite3
import os
import json
import sys


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
        sys.exit(msg)


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


class BibleClient:
    def __init__(self, book, chapter, verse, translation, format, verse_numbers):
        self.book = self.book = get_book_from_abbreviation(book)
        self.chapter = chapter
        self.verse = verse
        self.translation = translation
        self.format = format
        self.verse_numbers = verse_numbers
        self.cursor = self.get_bible_cursor()

    def create_empty_markdown_link(self):
        """Creates an empty link since mapping a book's abbreviation to
        a URL path variable would be overly complex.
        """
        link = f"([{self.book}"
        
        if self.chapter:
            link += f" {self.chapter}"
            
            if self.verse:
                link += f":{self.verse}"
        
        link += f" {self.translation}]())"
        
        return link

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
    def print_wall_of_text(self, verse_records): 
        verses = ''
        for row in verse_records:
            # Skip empty verses so orphaned verse numbers or extra whitespace
            # is not displayed
            if not row['text']:
                continue
            if self.verse_numbers:
                verses += str(row['verse']) + ' '
            
            verses += row['text'].strip() + ' '
        
        verses_split = list_multiline_verse(verses)
        wrapped_verses = '\n'.join(verses_split)
        
        print(wrapped_verses)

    # TODO: Print paragraphs from Bible format
    def print_markdown_excerpt(self, verse_records):
        """Generate Markdown excerpt for the verses.

        Args:
            verse_records (_type_): _description_
            params (_type_): _description_
        """
        print('###\n')
        print('______________________________________________________________________\n')
        self.print_wall_of_text(verse_records)
        print(self.create_empty_markdown_link())
        print('\n______________________________________________________________________')

    # TODO: Print paragraphs from Bible format
    # TODO: Parse USFM tags to create more readable passages/newlines
    def print_passage_by_format(self, verse_records):
        match self.format: 
            case 'txt':
                self.print_wall_of_text(verse_records)

            case 'md':
                self.print_markdown_excerpt(verse_records)

    def get_bible_cursor(self):
        database = f"{get_source_root()}/data/{self.translation}.db"
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        # TODO: Use context manager?
        return conn.cursor()

    def print_book(self):
        params = {'book': self.book}
    
        self.cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        """, params)

        verse_records = self.cursor.fetchall()
        
        self.print_passage_by_format(verse_records)

    def print_chapter(self):
        params = {'book': self.book, 'chapter': self.chapter}
        
        self.cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        """, params)

        verse_records = self.cursor.fetchall()
        
        if len(verse_records) == 0:
            msg = f"Invalid chapter: {self.book} {self.chapter}"
            print(msg)
        
        else:
            self.print_passage_by_format(verse_records)

    def print_verse(self):
        params = {
            'book': self.book,
            'chapter': self.chapter,
            'verse': self.verse
        }
        
        self.cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        AND verse = :verse
        """, params)

        verse_records = self.cursor.fetchall()
        
        if len(verse_records) == 0:
            msg = f"Invalid verse: {self.book} {self.chapter}:{self.verse}"
            print(msg)
        
        else:
            self.print_passage_by_format(verse_records)

    def print_verses(self):
        """
        Print a range of verses, eg. 5-7. 
        """
        
        verses = self.verse.split('-')
        self.verse_start = verses[0]
        self.verse_end = verses[1]
        
        params = {
            'book': self.book,
            'chapter': self.chapter,
            'verse_start': self.verse_start,
            'verse_end': self.verse_end,
        }
        
        
        self.cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        AND verse BETWEEN :verse_start AND :verse_end
        """, params)

        verse_records = self.cursor.fetchall()
        
        if len(verse_records) == 0:
            msg = (
                f"Invalid verses: {self.book} "
                f"{self.chapter}:{self.verse_start}-{self.verse_end}"
            )
            print(msg)
        
        else:
            self.print_passage_by_format(verse_records)
        
        # TODO: Use FTS4 SQLite extension to search bible for particular words/phrases
        # TODO: Fuzzy search? (eg. sanctify, sanctification, sanctity)
        def search_bible():
            pass
