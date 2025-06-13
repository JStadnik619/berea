import sqlite3
import os
import json
import csv
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


def import_resource_books(resource='step_bible'):
    books = []
    
    with open(f'{get_source_root()}/data/{resource}_books.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            books.append(row['abbreviation'])
    
    return books


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


def parse_verses_str(verses):
    verses_split = verses.split('-')
    return verses_split[0], verses_split[1]


class BibleClient:
    def __init__(self, book, chapter, verse, translation, format='txt', verse_numbers=False):
        self.book = self.book = get_book_from_abbreviation(book)
        self.chapter = chapter
        self.verse = verse
        self.translation = translation
        self.format = format
        self.verse_numbers = verse_numbers
        self.cursor = self.get_bible_cursor()

    def create_link_label(self):
        """Creates a link label, eg. `Isaiah 14:12-20`
        """
        label = self.book
        
        if self.chapter:
            label += f" {self.chapter}"
            
            if self.verse:
                label += f":{self.verse}"
        
        label += f" {self.translation}"
        
        return label
    
    def create_abbreviations_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS abbreviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            abbreviation TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
        """)
        
        books_to_abbreviations = {}
        
        with open(f'{get_source_root()}/data/book_abbreviations.json') as file:
            books_to_abbreviations = dict(json.load(file))
        
        # TODO: Get book ids from books table
        
        # TODO: Create a single query to add all book abbreviations 
        # This is the named style used with executemany():
        data = (
            {},
        )
        self.cursor.executemany("INSERT INTO abbreviations VALUES(:abbreviation, :book_id)", data)
        

    def create_resource_tables(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
        """)
        
        self.cursor.execute(f"""
        INSERT INTO resources (name) VALUES (
            stepbible.org
        );
        """)
        
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS resources_abbreviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER,
            abbreviation_id INTEGER
        );
        """)
        
        resource = 'STEP Bible'
        books = import_resource_books()
        
        # SELECT STEP Bible and abbreviation ids
        self.cursor.execute(f"""
        INSERT INTO resources_abbreviations (name) VALUES (
            stepbible.org
        );
        """)
    
    def get_book_abbreviation_by_resource(self, resource):
        """Get a book's abbreviation used by a specific resource.
        """
   
        params = {
            'book': self.book,
            'resource': resource,
        }
        
        # TODO: Implement these tables in db
        self.cursor.execute("""
            SELECT name FROM abbreviations
            JOIN books ON abbreviations.book_id = books.id
            JOIN resource_abbreviations ON resource_abbreviations.abbreviation_id = abbreviations.id
            JOIN resources ON resource_abbreviations.resource_id = resources.id
            WHERE books.name = :book
            AND resources.name = :resource
            """, params)
        
        # Assuming a resource only has one abbreviation for a given book and translation
        return self.cursor.fetchone()[0]
    
    # TODO: Link format depends on resource
    def create_link(self, resource='stepbible.org'):
        book_abbrev = self.get_book_abbreviation_by_resource(self.book, resource)
        
        link = self.book
        
        if self.verse:

            # Parse verses if multiple provided
            if self.verse.contains('-'):
                verse_start, verse_end = parse_verses_str(self.verse)
                link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}.{self.chapter}.{verse_start}-{book_abbrev}.{self.chapter}.{verse_end}&options=VNHUG"
                
            else:
                link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}.{self.chapter}.{self.verse}&options=NVHUG"
        
        elif self.chapter:
            link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}.{self.chapter}&options=NVHUG"
        
        # Make link for whole book
        else:
            link = f"https://www.stepbible.org/?q=version={self.translation}@reference={book_abbrev}&options=NVHUG"
        
        # TODO: Ping link and raise error if not valid?
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
        print(f"([{self.create_link_label()}]({self.create_link()}))")
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
        
        verse_start, verse_end = parse_verses_str(self.verse)
        
        params = {
            'book': self.book,
            'chapter': self.chapter,
            'verse_start': verse_start,
            'verse_end': verse_end,
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
                f"{self.chapter}:{verse_start}-{verse_end}"
            )
            print(msg)
        
        else:
            self.print_passage_by_format(verse_records)
        
        # TODO: Use FTS4 SQLite extension to search bible for particular words/phrases
        # TODO: Fuzzy search? (eg. sanctify, sanctification, sanctity)
        def search_bible():
            pass
