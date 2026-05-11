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
        # TODO: Find example for Markup ending with ! ? : ; not separated by a space.
        (
            "Poetry within a paragraph is not rendered properly.",
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
            "Poetry of consecutive q1's and q2's (some empty) are not properly formatted.",
            [
                {"book": "Psalms", "chapter": 117, "verse": 1, "text": "Praise the LORD, all you nations!", "type": "para", "marker": "q1"},
                {"book": "Psalms", "chapter": 117, "verse": 1, "text": "Extol Him, all you peoples!", "type": "para", "marker": "q2"},
                {"book": "Psalms", "chapter": 117, "verse": 1, "text": "", "type": "para", "marker": "q2"},
                {"book": "Psalms", "chapter": 117, "verse": 1, "text": "For great is His loving devotion toward us,", "type": "para", "marker": "q1"},
                {"book": "Psalms", "chapter": 117, "verse": 1, "text": "and the faithfulness of the LORD endures forever.", "type": "para", "marker": "q2"},
                {"book": "Psalms", "chapter": 117, "verse": 2, "text": "", "type": "para", "marker": "b"},
                {"book": "Psalms", "chapter": 117, "verse": 1, "text": "Hallelujah!", "type": "para", "marker": "q1"},
                {"book": "Psalms", "chapter": 117, "verse": 1, "text": "", "type": "para", "marker": "q1"},
            ],
            (
                "Praise the LORD, all you nations!\n"
                "  Extol Him, all you peoples!\n"
                "For great is His loving devotion toward us,\n"
                "  and the faithfulness of the LORD endures forever.\n"
                "\n"
                "Hallelujah!"
            )
        ),
        (
            # TODO: Poetry line containing footnote is not concatenated.
            "Empty poetry lines are not omitted.",
            [
                {"book": "Proverbs", "chapter": 1, "verse": 1, "text": "These are the proverbs of Solomon son of David,", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 1, "text": "king of Israel,", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 2, "text": "for gaining wisdom and discipline,", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 2, "text": "for comprehending words of insight,", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 3, "text": "and for receiving instruction in wise living", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 3, "text": "and in righteousness, justice, and equity.", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 4, "text": "To impart prudence to the simple", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 4, "text": "", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 4, "text": "and knowledge and discretion to the young,", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 5, "text": "let the wise listen and gain instruction,", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 5, "text": "and the discerning acquire wise counsel", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 6, "text": "by understanding the proverbs and parables,", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 6, "text": "the sayings and riddles of the wise.", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 6, "text": "", "type": "para", "marker": "b"},
                {"book": "Proverbs", "chapter": 1, "verse": 6, "text": "The fear of the LORD is the beginning of knowledge,", "type": "para", "marker": "q1"},
                {"book": "Proverbs", "chapter": 1, "verse": 6, "text": "but fools", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 6, "text": " despise wisdom and discipline.", "type": "para", "marker": "q2"},
                {"book": "Proverbs", "chapter": 1, "verse": 7, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "These are the proverbs of Solomon son of David,\n"
                "  king of Israel,\n"
                "for gaining wisdom and discipline,\n"
                "  for comprehending words of insight,\n"
                "and for receiving instruction in wise living\n"
                "  and in righteousness, justice, and equity.\n"
                "To impart prudence to the simple\n"
                "  and knowledge and discretion to the young,\n"
                "let the wise listen and gain instruction,\n"
                "  and the discerning acquire wise counsel\n"
                "by understanding the proverbs and parables,\n"
                "  the sayings and riddles of the wise.\n"
                "\n"
                "The fear of the LORD is the beginning of knowledge,\n"
                # TODO: This poetry line gets split when parsed because it contains a footnote
                "  but fools\n"
                "   despise wisdom and discipline."
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
        (
            "Line numbers of contiguous verses are not separated by spaces.",
            [
                {"book": "John", "chapter": 1, "verse": 1, "text": "In the beginning was the Word, and the Word was with God, and the Word was God.", "type": "para", "marker": "m"},
                {"book": "John", "chapter": 1, "verse": 2, "text": "He was with God in the beginning.", "type": "para", "marker": "m"},
                {"book": "John", "chapter": 1, "verse": 3, "text": "Through Him all things were made, and without Him nothing was made that has been made.", "type": "para", "marker": "m"},
                {"book": "John", "chapter": 1, "verse": 4, "text": "In Him was life, and that life was the light of men.", "type": "para", "marker": "m"},
                {"book": "John", "chapter": 1, "verse": 5, "text": "The Light shines in the darkness, and the darkness has not overcome", "type": "para", "marker": "m"},
                {"book": "John", "chapter": 1, "verse": 5, "text": " it.", "type": "para", "marker": "m"},
                {"book": "John", "chapter": 1, "verse": 5, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "1 In the beginning was the Word, and the Word was with God, and the Word was\n"
                "God. 2 He was with God in the beginning. 3 Through Him all things were made, and\n"
                "without Him nothing was made that has been made. 4 In Him was life, and that\n"
                "life was the light of men. 5 The Light shines in the darkness, and the darkness\n"
                "has not overcome it."
            ),
        ),
    ]
)    
def test_render_markup_verse_mumbers(msg, markup_records, rendered_passage):
    assert render_markup(markup_records, verse_numbers=True) == rendered_passage, msg
