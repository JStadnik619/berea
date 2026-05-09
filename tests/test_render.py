import pytest

from berea.render import (
    list_multiline_verse,
    render_markup
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
    "msg, markup_records, rendered_passage",
    [
        (
            "Blocks of lines in list items are not properly formatted.",
            [
                {"book": "GEN", "chapter": 2, "verse": 10, "text": "", "type": "verse", "marker": "v"},
                {"book": "GEN", "chapter": 2, "verse": 10, "text": "Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters:", "type": "para", "marker": "m"},
                {"book": "GEN", "chapter": 2, "verse": 10, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 11, "text": "", "type": "verse", "marker": "v"},
                {"book": "GEN", "chapter": 2, "verse": 11, "text": "The name of the first river is the Pishon; it winds through the whole land of Havilah, where there is gold.", "type": "para", "marker": "li1"},

                {"book": "GEN", "chapter": 2, "verse": 12, "text": "", "type": "verse", "marker": "v"},
                {"book": "GEN", "chapter": 2, "verse": 12, "text": "And the gold of that land is pure, and bdellium and onyx are found there.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 12, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 13, "text": "", "type": "verse", "marker": "v"},
                {"book": "GEN", "chapter": 2, "verse": 13, "text": "The name of the second river is the Gihon; it winds through the whole land of Cush.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 13, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 14, "text": "", "type": "verse", "marker": "v"},
                {"book": "GEN", "chapter": 2, "verse": 14, "text": "The name of the third river is the Tigris; it runs along the east side of Assyria.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 14, "text": "", "type": "para", "marker": "b"},
                {"book": "GEN", "chapter": 2, "verse": 14, "text": "And the fourth river is the Euphrates.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 14, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 15, "text": "", "type": "verse", "marker": "v"},
                {"book": "GEN", "chapter": 2, "verse": 15, "text": "Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it.", "type": "para", "marker": "m"},
                {"book": "GEN", "chapter": 2, "verse": 15, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "Now a river flowed out of Eden to water the garden, and from there it branched\n"
                "into four headwaters:\n"
                "\n"
                "  The name of the first river is the Pishon; it winds through the whole land of\n"
                "  Havilah, where there is gold. And the gold of that land is pure, and bdellium\n"
                "  and onyx are found there.\n"
                "\n"
                "  The name of the second river is the Gihon; it winds through the whole land of\n"
                "  Cush.\n"
                "\n"
                "  The name of the third river is the Tigris; it runs along the east side of\n"
                "  Assyria.\n"
                "\n"
                "  And the fourth river is the Euphrates.\n"
                "\n"
                "Then the LORD God took the man and placed him in the Garden of Eden to cultivate\n"
                "and keep it."
            ),
        ),
        (
            "Sentences within the same paragraph are not separated by a space.",
            [
                {"book": "GEN", "chapter": 1, "verse": 3, "text": "And God said, “Let there be light,”", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 3, "text": " and there was light.", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 4, "text": "And God saw that the light was good, and He separated the light from the darkness.", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 5, "text": "God called the light “day,” and the darkness He called “night.”", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 5, "text": "", "type": "para", "marker": "b"},
                {"book": "GEN", "chapter": 1, "verse": 5, "text": "And there was evening, and there was morning—the first day.", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 5, "text": "", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 5, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "And God said, “Let there be light,” and there was light. And God saw that the\n"
                "light was good, and He separated the light from the darkness. God called the\n"
                "light “day,” and the darkness He called “night.”\n"
                "\n"
                "And there was evening, and there was morning—the first day."
            )
        ),
        (
            "Clauses across verses within the same sentence are not separated by a space.",
            [
                {"book": "GEN", "chapter": 1, "verse": 17, "text": "God set these lights in the expanse of the sky to shine upon the earth,", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 18, "text": "to preside over the day and the night, and to separate the light from the darkness. And God saw that it was good.", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 18, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "God set these lights in the expanse of the sky to shine upon the earth, to\n"
                "preside over the day and the night, and to separate the light from the darkness.\n"
                "And God saw that it was good."
            )
        ),
        (
            "Verses ending with quotes are not separated by a space.",
            [
                {"book": "GEN", "chapter": 1, "verse": 20, "text": "And God said, “Let the waters teem with living creatures, and let birds fly above the earth in the open expanse of the sky.”", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 21, "text": "So God created the great sea creatures and every living thing that moves, with which the waters teemed according to their kinds, and every winged bird after its kind. And God saw that it was good.", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 21, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "And God said, “Let the waters teem with living creatures, and let birds fly\n"
                "above the earth in the open expanse of the sky.” So God created the great sea\n"
                "creatures and every living thing that moves, with which the waters teemed\n"
                "according to their kinds, and every winged bird after its kind. And God saw that\n"
                "it was good."
            )
        ),
        (
            "Poetry is not rendered properly.",
            [
                {"book": "GEN", "chapter": 1, "verse": 26, "text": "Then God said, “Let Us make man in Our image, after Our likeness, to rule over the fish of the sea and the birds of the air, over the livestock, and over all the earth itself", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 26, "text": " and every creature that crawls upon it.”", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 26, "text": "", "type": "para", "marker": "b"},
                {"book": "GEN", "chapter": 1, "verse": 27, "text": "So God created man in His own image;", "type": "para", "marker": "q1"},
                {"book": "GEN", "chapter": 1, "verse": 27, "text": "in the image of God He created him;", "type": "para", "marker": "q2"},
                {"book": "GEN", "chapter": 1, "verse": 27, "text": "male and female He created them.", "type": "para", "marker": "q2"},
                {"book": "GEN", "chapter": 1, "verse": 27, "text": "", "type": "para", "marker": "q2"},
                {"book": "GEN", "chapter": 1, "verse": 27, "text": "", "type": "para", "marker": "b"},
                {"book": "GEN", "chapter": 1, "verse": 28, "text": "God blessed them and said to them, “Be fruitful and multiply, and fill the earth and subdue it; rule over the fish of the sea and the birds of the air and every creature that crawls upon the earth.”", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 28, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "Then God said, “Let Us make man in Our image, after Our likeness, to rule over\n"
                "the fish of the sea and the birds of the air, over the livestock, and over all\n"
                "the earth itself and every creature that crawls upon it.”\n"
                "\n"
                "So God created man in His own image;\n"
                "  in the image of God He created him;\n"
                "  male and female He created them.\n"
                "\n"
                "God blessed them and said to them, “Be fruitful and multiply, and fill the earth\n"
                "and subdue it; rule over the fish of the sea and the birds of the air and every\n"
                "creature that crawls upon the earth.”"
            )
        ),
        (
            "Failed to render all markup records of a verse without a trailing newline.",
            [
                {"book": "GEN", "chapter": 1, "verse": 31, "text": "And God looked upon all that He had made, and indeed, it was very good.", "type": "para", "marker": "pmo"},
                {"book": "GEN", "chapter": 1, "verse": 31, "text": "", "type": "para", "marker": "b"},
                {"book": "GEN", "chapter": 1, "verse": 31, "text": "And there was evening, and there was morning—the sixth day.", "type": "para", "marker": "pmo"},
            ],
            (
                "And God looked upon all that He had made, and indeed, it was very good.\n"
                "\n"
                "And there was evening, and there was morning—the sixth day."
            )
        ),
    ]
)
def test_render_markup(msg, markup_records, rendered_passage):
    assert render_markup(markup_records) == rendered_passage, msg

@pytest.mark.parametrize(
    "msg, markup_records, rendered_passage",
    [
        (
            "Blocks of lines in list items are not properly formatted.",
            [
                {"book": "GEN", "chapter": 2, "verse": 10, "text": "Now a river flowed out of Eden to water the garden, and from there it branched into four headwaters:", "type": "para", "marker": "m"},
                {"book": "GEN", "chapter": 2, "verse": 10, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 11, "text": "The name of the first river is the Pishon; it winds through the whole land of Havilah, where there is gold.", "type": "para", "marker": "li1"},

                {"book": "GEN", "chapter": 2, "verse": 12, "text": "And the gold of that land is pure, and bdellium and onyx are found there.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 12, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 13, "text": "The name of the second river is the Gihon; it winds through the whole land of Cush.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 13, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 14, "text": "The name of the third river is the Tigris; it runs along the east side of Assyria.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 14, "text": "", "type": "para", "marker": "b"},
                {"book": "GEN", "chapter": 2, "verse": 14, "text": "And the fourth river is the Euphrates.", "type": "para", "marker": "li1"},
                {"book": "GEN", "chapter": 2, "verse": 14, "text": "", "type": "para", "marker": "b"},

                {"book": "GEN", "chapter": 2, "verse": 15, "text": "Then the LORD God took the man and placed him in the Garden of Eden to cultivate and keep it.", "type": "para", "marker": "m"},
                {"book": "GEN", "chapter": 2, "verse": 15, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "10 Now a river flowed out of Eden to water the garden, and from there it\n"
                "branched into four headwaters:\n"
                "\n"
                "  11 The name of the first river is the Pishon; it winds through the whole land\n"
                "  of Havilah, where there is gold. 12 And the gold of that land is pure, and\n"
                "  bdellium and onyx are found there.\n"
                "\n"
                "  13 The name of the second river is the Gihon; it winds through the whole land\n"
                "  of Cush.\n"
                "\n"
                "  14 The name of the third river is the Tigris; it runs along the east side of\n"
                "  Assyria.\n"
                "\n"
                "  And the fourth river is the Euphrates.\n"
                "\n"
                "15 Then the LORD God took the man and placed him in the Garden of Eden to\n"
                "cultivate and keep it."
            ),
        ),
    ]
)    
def test_render_markup_verse_mumbers(msg, markup_records, rendered_passage):
    assert render_markup(markup_records, verse_numbers=True) == rendered_passage, msg
