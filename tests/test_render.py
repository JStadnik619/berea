import pytest

from berea.render import list_multiline_verse


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
