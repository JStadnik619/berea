import urllib.request
import os

import pytest

from biblecli.bible import list_multiline_verse, BibleClient, get_source_root


@pytest.mark.parametrize(
    "verse, verse_list",
    [   
        # John 3:16 KJV (141 characters)
        (
            "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
            [
                "For God so loved the world, that he gave his only begotten Son, that whosoever",
                "believeth in him should not perish, but have everlasting life."
            ]
        ),
        # Esther 8:9 KJV (528 characters)
        (
            "Then were the king’s scribes called at that time in the third month, that is, the month Sivan, on the three and twentieth day thereof; and it was written according to all that Mordecai commanded unto the Jews, and to the lieutenants, and the deputies and rulers of the provinces which are from India unto Ethiopia, an hundred twenty and seven provinces, unto every province according to the writing thereof, and unto every people after their language, and to the Jews according to their writing, and according to their language.",
            [
                "Then were the king’s scribes called at that time in the third month, that is,",
                "the month Sivan, on the three and twentieth day thereof; and it was written",
                "according to all that Mordecai commanded unto the Jews, and to the",
                "lieutenants, and the deputies and rulers of the provinces which are from India",
                "unto Ethiopia, an hundred twenty and seven provinces, unto every province",
                "according to the writing thereof, and unto every people after their language,",
                "and to the Jews according to their writing, and according to their language."
            ]
        ),
    ]
)
def test_list_multiline_verse(verse, verse_list):
    assert list_multiline_verse(verse) == verse_list


def valid_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return True
            else:
                return False
    except urllib.error.HTTPError as e:
        print("HTTP error:", e.code)
        return False
    except urllib.error.URLError as e:
        print("URL error:", e.reason)
        return False


@pytest.mark.parametrize(
    "msg, book, chapter, verse, translation, expected_link",
    [
        (
            "Creating link for a single verse failed",
            "John", "3", "16", "BSB",
            "https://www.stepbible.org/?q=version=BSB@reference=john.3.16&options=NVHUG"
        ),
        (
            "Creating link for multiple verses failed",
            "John", "3", "16-18", "BSB",
            "https://www.stepbible.org/?q=version=BSB@reference=john.3.16-john.3.18&options=NVHUG"
        ),
        (
            "Creating link for a chapter failed",
            "Psalms", "117", None, "BSB",
            "https://www.stepbible.org/?q=version=BSB@reference=psalm.117&options=NVHUG"
        ),
        (
            "Creating link for a book",
            "III John", None, None, "BSB",
            "https://www.stepbible.org/?q=version=BSB@reference=3john&options=NVHUG"
        ),
    ]
)
def test_create_link(msg, book, chapter, verse, translation, expected_link):
    bible = BibleClient(translation)
    actual_link = bible.create_link(book, chapter, verse)
    assert actual_link == expected_link, msg
    assert valid_url(actual_link)


def test_validate_resource_abbreviations():
    """Creating links from the resource's book abbreviations yields valid URLs."""
    bible = BibleClient('BSB')
    
    books = bible.get_bible_cursor().execute("SELECT * FROM books").fetchall()
    
    for book in books:
        link = bible.create_link(book['name'])
        assert valid_url(link), f"{book['name']} produced invalid link: {link}"


@pytest.mark.parametrize(
    "translation",
    [
        ('KJV'),
        ('BSB'),
        ('RLT'),        
        ('UKJV'),        
    ]
)
def test_create_bible_db(tmp_path, translation):
    bible = BibleClient(translation)
    bible.database = f"{tmp_path}/{translation}.db"

    bible.create_bible_db()

    cursor = bible.get_bible_cursor()

    assert os.path.isfile(bible.database), 'Downloading the translation database failed.'

    actual_tables = [row['name'] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]

    table_record_counts = {
        'books': 66,
        'verses': 31102,
    }

    msg = 'Renaming the database tables failed.'
    renamed_tables = table_record_counts.keys()
    assert set(renamed_tables).issubset(actual_tables), msg

    for table, expected_records_count in table_record_counts.items():
        sql = f"SELECT COUNT(*) FROM {table};"
        actual_records_count = cursor.execute(sql).fetchone()[0]
        assert actual_records_count == expected_records_count, f"'{table}' table does not contain expected record count."

    created_tables = ['abbreviations', 'resources', 'resources_abbreviations']
    for expected_table in created_tables:
        assert expected_table in actual_tables, f"'{expected_table}' table does not exist."


# TODO: Move this test to test_cli.py
@pytest.mark.parametrize(
    "msg, phrase, output",
    [
        (
            "Searching a phrase with a single occurrence failed",
            'rescue my soul',
            (
                "1 occurrences of 'rescue my soul' in the BSB Bible:\n"
                "___\n"
                "\nPsalms 35:17:\n"
                "How long, O Lord, will You look on? Rescue my soul from their ravages, my precious life from these lions. \n"
                "___\n"
            )
        ),
        (
            "Searching a phrase with multiple occurrences failed",
            'sheep gate',
            (
                "4 occurrences of 'sheep gate' in the BSB Bible:\n"
                "___\n\n"
                "Nehemiah 3:1:\n"
                "At the Sheep Gate, Eliashib the high priest and his fellow priests began rebuilding. They dedicated it and installed its doors. After building as far as the Tower of the Hundred and the Tower of Hananel, they dedicated the wall. \n"
                "___\n\n"
                "Nehemiah 3:32:\n"
                "And between the upper room above the corner and the Sheep Gate, the goldsmiths and merchants made repairs. \n"
                "___\n\n"
                "Nehemiah 12:39:\n"
                "over the Gate of Ephraim, the Jeshanah Gate, the Fish Gate, the Tower of Hananel, and the Tower of the Hundred, as far as the Sheep Gate. And they stopped at the Gate of the Guard. \n"
                "___\n\n"
                "John 5:2:\n"
                "Now there is in Jerusalem near the Sheep Gate a pool with five covered colonnades, which in Hebrew is called Bethesda. \n"
                "___\n"
            )
        ),
    ]
)
def test_search(capsys, msg, phrase, output):
    bible = BibleClient('BSB')
    bible.search(phrase)
    
    captured = capsys.readouterr()
    assert captured.out == output + '\n', msg
