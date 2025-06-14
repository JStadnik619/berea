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
    # print args:
    # book, chapter, verse, format='txt', verse_numbers=False
    def __init__(self, translation):
        self.translation = translation
        self.cursor = self.get_bible_cursor()
        self.database = f"{get_source_root()}/data/{self.translation}.db"
    
    def get_bible_cursor(self):
        database = f"{get_source_root()}/data/{self.translation}.db"
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        # TODO: Use context manager?
        return conn.cursor()

    def create_link_label(self, book, chapter=None, verse=None):
        """Creates a link label, eg. `Isaiah 14:12-20`
        """
        label = book
        
        if chapter:
            label += f" {chapter}"
            
            if verse:
                label += f":{verse}"
        
        label += f" {self.translation}"
        
        return label
    
    def create_abbreviations_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS abbreviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            abbreviation TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
        """)
        
        books_to_abbreviations = {}
        
        with open(f'{get_source_root()}/data/book_abbreviations.json') as file:
            books_to_abbreviations = dict(json.load(file))
    
        # TODO: Create a single query to add all book abbreviations 
        
        # Create a conn to commit inserts and close 
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        for book, abbreviations in books_to_abbreviations.items():
            for abbreviation in abbreviations:
                params = {
                    'abbreviation': abbreviation,
                    'book': book,
                }
                
                cursor.execute(f"""
                INSERT INTO abbreviations (abbreviation, book_id)
                SELECT :abbreviation, books.id
                FROM books
                WHERE books.name = :book;
                """, params)
        
        conn.commit()
        conn.close()

    def create_resource_tables(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
        """)
        
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS resources_abbreviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER,
            abbreviation_id INTEGER
        );
        """)
        
        # Create a conn to commit inserts and close 
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        # TODO: Insert STEP Bible dynamically
        resource='STEP Bible'
        cursor.execute(f"""
        INSERT INTO resources (name) VALUES (
            'STEP Bible'
        );
        """)
        
        conn.commit()
        conn.close()
        
        abbreviations = import_resource_books()
        
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        for abbreviation in abbreviations:
            params = {
                'abbreviation': abbreviation.lower(),
            }
            
            # TODO: Select STEP Bible id dynamically
            cursor.execute(f"""
            INSERT INTO resources_abbreviations (resource_id, abbreviation_id)
            SELECT 1, abbreviations.id
            FROM abbreviations
            WHERE abbreviations.abbreviation = :abbreviation;
            """, params)
        
        conn.commit()
        conn.close()
    
    def get_book_abbreviation_by_resource(self, book, resource):
        """Get a book's abbreviation used by a specific resource.
        """
   
        params = {
            'book': book,
            'resource': resource,
        }
        
        self.cursor.execute("""
            SELECT abbreviation FROM abbreviations
            JOIN books ON abbreviations.book_id = books.id
            JOIN resources_abbreviations ON resources_abbreviations.abbreviation_id = abbreviations.id
            JOIN resources ON resources_abbreviations.resource_id = resources.id
            WHERE books.name = :book
            AND resources.name = :resource
            """, params)
        
        # Assuming a resource only has one abbreviation for a given book and translation
        return self.cursor.fetchone()[0]
    
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
    def print_wall_of_text(self, verse_records, verse_numbers=False): 
        verses = ''
        for row in verse_records:
            # Skip empty verses so orphaned verse numbers or extra whitespace
            # is not displayed
            if not row['text']:
                continue
            if verse_numbers:
                verses += str(row['verse']) + ' '
            
            verses += row['text'].strip() + ' '
        
        verses_split = list_multiline_verse(verses)
        wrapped_verses = '\n'.join(verses_split)
        
        print(wrapped_verses)

    # TODO: Print paragraphs from Bible format
    def print_markdown_excerpt(self, verse_records, book, chapter, verse):
        """Generate Markdown excerpt for the verses.

        Args:
            verse_records (_type_): _description_
            params (_type_): _description_
        """
        print('###\n')
        print('______________________________________________________________________\n')
        self.print_wall_of_text(verse_records)
        print(
            f"([{self.create_link_label(book, chapter, verse,)}]"
            f"({self.create_link(book, chapter, verse,)}))"
        )
        print('\n______________________________________________________________________')

    # TODO: Print paragraphs from Bible format
    # TODO: Parse USFM tags to create more readable passages/newlines
    def print_passage_by_format(self, format, verse_records, verse_numbers=False, book=None, chapter=None, verse=None):
        match format: 
            case 'txt':
                self.print_wall_of_text(verse_records, verse_numbers)

            case 'md':
                self.print_markdown_excerpt(verse_records, book, chapter, verse)

    def print_book(self, book, format, verse_numbers):
        book = get_book_from_abbreviation(book)
        params = {'book': book}
    
        self.cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        """, params)

        verse_records = self.cursor.fetchall()
        
        self.print_passage_by_format(
            format,
            verse_records,
            verse_numbers=verse_numbers,
            book=book
        )

    def print_chapter(self, book, chapter, format, verse_numbers):
        book = get_book_from_abbreviation(book)
        params = {'book': book, 'chapter': chapter}
        
        self.cursor.execute("""
        SELECT verse, text FROM verses
        JOIN books ON verses.book_id = books.id
        WHERE books.name = :book
        AND chapter = :chapter
        """, params)

        verse_records = self.cursor.fetchall()
        
        if len(verse_records) == 0:
            msg = f"Invalid chapter: {book} {chapter}"
            print(msg)
        
        else:
            self.print_passage_by_format(
                format,
                verse_records,
                verse_numbers=verse_numbers,
                book=book,
                chapter=chapter
            )

    def print_verse(self, book, chapter, verse, format, verse_numbers):
        book = get_book_from_abbreviation(book)
        params = {
            'book': book,
            'chapter': chapter,
            'verse': verse
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
            msg = f"Invalid verse: {book} {chapter}:{verse}"
            print(msg)
        
        else:
            self.print_passage_by_format(
                format,
                verse_records,
                verse_numbers=verse_numbers,
                book=book,
                chapter=chapter,
                verse=verse
            )

    def print_verses(self, book, chapter, verse, format, verse_numbers):
        """
        Print a range of verses, eg. 5-7. 
        """
        book = get_book_from_abbreviation(book)
        verse_start, verse_end = parse_verses_str(verse)
        
        params = {
            'book': book,
            'chapter': chapter,
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
                f"Invalid verses: {book} "
                f"{chapter}:{verse_start}-{verse_end}"
            )
            print(msg)
        
        else:
            self.print_passage_by_format(
                format,
                verse_records,
                verse_numbers=verse_numbers,
                book=book,
                chapter=chapter,
                verse=verse
            )
        
        # TODO: Use FTS4 SQLite extension to search bible for particular words/phrases
        # TODO: Fuzzy search? (eg. sanctify, sanctification, sanctity)
        def search_bible():
            pass
