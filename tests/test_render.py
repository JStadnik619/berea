import pytest

from berea.render import (
    list_multiline_verse,
    replace_usfm,
    verses_to_formatted_passage
)


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


@pytest.mark.parametrize(
    "verse, rendered_verse",
    [
        (
            "So God created man in His own image;\q2 in the image of God He created him;\q2 male and female He created them.",
            "So God created man in His own image;\n   in the image of God He created him;\n   male and female He created them.",
        ),
    ]
)
def test_replace_usfm(verse, rendered_verse):
    assert replace_usfm(verse) == rendered_verse


@pytest.mark.parametrize(
    "verse_records, formatted_passage",
    [
        # Passage with newlines and list items (BSB Gen 2:10-15)
        (
            [
                {
                    'verse': 10,
                    # Blank lines would have to be appended to verses
                    'text': "Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters:\b",
                },
                {
                    'verse': 11,
                    # List items would have to be prepended to verses
                    'text': "\li1The name of the first river is Pishon; it winds through the whole land of Havilah, where there is gold.",
                },
                {
                    'verse': 12,
                    'text': "And the gold of that land is pure, and bdellium and onyx are found there.\b",
                },
                {
                    'verse': 13,
                    'text': "\li1The name of the second river is Gihon; it winds through the whole land of Cush.\b",
                },
                {
                    'verse': 14,
                    'text': "\liThe name of the third river is Hiddekel; it runs along the east side of Assyria.\b \li1And the fourth river is the Euphrates.\b",
                },
                {
                    'verse': 15,
                    'text': "Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it.\b",
                },
            ],
            # Lines should be wrapped to 80 characters
            # Newlines should appear before verses 11, 13, 14, and 15
            # Verse 14 section "And the fourth river is the Euphrates." should be preceded by a newline
            # Verses 11-14 should be indented by two spaces
            # This may need to be adjusted for
            (
                "Now a river flowed out of Eden to water the garden, and from there it\n"
                "branched into four headwaters:\n"
                "\n"
                "  The name of the first river is the Pishon; it winds through the whole\n"
                "  land of Havilah, where there is gold. And the gold of that land is pure,\n"
                "  and bdellium and onyx are found there.\n"
                "\n"
                "  The name of the second river is the Gihon; it winds through the whole\n"
                "  land of Cush.\n"
                "\n"
                "  The name of the third river is the Tigris; it runs along the east side\n"
                "  of Assyria.\n"
                "\n"
                "  And the fourth river is the Euphrates.\n"
                "\n"
                "Then the LORD God took the man and placed him in the Garden of Eden to\n"
                "cultivate and keep it\n"
            )
        )
    ]
)
def test_verses_to_formatted_passage(verse_records, formatted_passage):
    assert verses_to_formatted_passage(verse_records, False, 'txt') == formatted_passage
