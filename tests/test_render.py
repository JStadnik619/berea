import pytest

from berea.render import (
    list_multiline_verse,
    render_markup,
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
            "Verses ending with an exclamation point are not separated by a space.",
            [
                {"book": "Revelation", "chapter": 3, "verse": 15, "text": "I know your deeds; you are neither cold nor hot. How I wish you were one or the other!", "type": "para", "marker": "pmo"},
                {"book": "Revelation", "chapter": 3, "verse": 16, "text": "So because you are lukewarm—neither hot nor cold—I am about to vomit you out of My mouth!", "type": "para", "marker": "pmo"},
                {"book": "Revelation", "chapter": 3, "verse": 16, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "I know your deeds; you are neither cold nor hot. How I wish you were one or the\n"
                "other! So because you are lukewarm—neither hot nor cold—I am about to vomit you\n"
                "out of My mouth!"
            )
        ),
        (
            "Verses ending with a question mark are not separated by a space.",
            [
                {"book": "James", "chapter": 4, "verse": 5, "text": "Or do you think the Scripture says without reason that the Spirit", "type": "para", "marker": "m"},
                {"book": "James", "chapter": 4, "verse": 5, "text": " He caused to dwell in us yearns with envy?", "type": "para", "marker": "m"},
                {"book": "James", "chapter": 4, "verse": 6, "text": "But He gives us more grace. This is why it says:", "type": "para", "marker": "m"},
                {"book": "James", "chapter": 4, "verse": 6, "text": "", "type": "para", "marker": "b"},
                {"book": "James", "chapter": 4, "verse": 6, "text": "“God opposes the proud,", "type": "para", "marker": "q1"},
                {"book": "James", "chapter": 4, "verse": 6, "text": "but gives grace to the humble.”", "type": "para", "marker": "q2"},
                {"book": "James", "chapter": 4, "verse": 6, "text": "", "type": "para", "marker": "q2"},
                {"book": "James", "chapter": 4, "verse": 6, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "Or do you think the Scripture says without reason that the Spirit He caused to\n"
                "dwell in us yearns with envy? But He gives us more grace. This is why it says:\n"
                "\n"
                "“God opposes the proud,\n"
                "  but gives grace to the humble.”"
            )
        ),
        (
            "Verses ending with a colon are not separated by a space.",
            [
                {"book": "1 John", "chapter": 2, "verse": 5, "text": "But if anyone keeps His word, the love of God has been truly perfected in him. By this we know that we are in Him:", "type": "para", "marker": "m"},
                {"book": "1 John", "chapter": 2, "verse": 5, "text": "Whoever claims to abide in Him must walk as Jesus walked.", "type": "para", "marker": "m"},
                {"book": "1 John", "chapter": 2, "verse": 6, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "But if anyone keeps His word, the love of God has been truly perfected in him.\n"
                "By this we know that we are in Him: Whoever claims to abide in Him must walk as\n"
                "Jesus walked."
            )
        ),
        (
            "Verses ending with a semicolon are not separated by a space.",
            [
                {"book": "Jude", "chapter": 1, "verse": 22, "text": "And indeed, have mercy on those who doubt;", "type": "para", "marker": "m"},
                {"book": "Jude", "chapter": 1, "verse": 23, "text": "save others by snatching them from the fire; and to still others show mercy tempered with fear, hating even the clothing stained by the flesh.", "type": "para", "marker": "m"},
                {"book": "Jude", "chapter": 1, "verse": 23, "text": "", "type": "para", "marker": "b"},
            ],
            (
                "And indeed, have mercy on those who doubt; save others by snatching them from the\n"
                "fire; and to still others show mercy tempered with fear, hating even the\n"
                "clothing stained by the flesh."
            )
        ),
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
        # BUG: The last q2 of matt 1 23 is split by a footnote
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
        # KJV Cambridge Paragraph Version
        (
            "Small-cap text and translator's additions aren't rendered properly.",
            [
                {"book": "Genesis", "chapter": 1, "verse": 1, "text": "In", "type": "char", "marker": "sc"},
                {"book": "Genesis", "chapter": 1, "verse": 1, "text": " the beginning God created the heaven and the earth.", "type": "para", "marker": "m"},
                {"book": "Genesis", "chapter": 1, "verse": 2, "text": "And the earth was without form, and void; and darkness", "type": "para", "marker": "m"},
                {"book": "Genesis", "chapter": 1, "verse": 2, "text": "was", "type": "char", "marker": "add"},
                {"book": "Genesis", "chapter": 1, "verse": 2, "text": " upon the face of the deep. And the Spirit of God moved upon the face of the waters.", "type": "para", "marker": "m"},
                {"book": "Genesis", "chapter": 1, "verse": 3, "text": "And God said, Let there be light: and there was light.", "type": "para", "marker": "p"},
                {"book": "Genesis", "chapter": 1, "verse": 4, "text": "And God saw the light, that", "type": "para", "marker": "p"},
                {"book": "Genesis", "chapter": 1, "verse": 4, "text": "it was", "type": "char", "marker": "add"},
                {"book": "Genesis", "chapter": 1, "verse": 4, "text": " good: and God divided the light from the darkness.", "type": "para", "marker": "p"},
            ],
            (
                "In the beginning God created the heaven and the earth. And the earth was without\n"
                "form, and void; and darkness was upon the face of the deep. And the Spirit of\n"
                "God moved upon the face of the waters. And God said, Let there be light: and\n"
                "there was light. And God saw the light, that it was good: and God divided the\n"
                "light from the darkness."
            )
        )
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
        (
            "Poetry of consecutive q1's and q2's (some empty) are not properly formatted.",
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
                "1 These are the proverbs of Solomon son of David,\n"
                "  king of Israel,\n"
                "2 for gaining wisdom and discipline,\n"
                "  for comprehending words of insight,\n"
                "3 and for receiving instruction in wise living\n"
                "  and in righteousness, justice, and equity.\n"
                "4 To impart prudence to the simple\n"
                "  and knowledge and discretion to the young,\n"
                "5 let the wise listen and gain instruction,\n"
                "  and the discerning acquire wise counsel\n"
                "6 by understanding the proverbs and parables,\n"
                "  the sayings and riddles of the wise.\n"
                "\n"
                "The fear of the LORD is the beginning of knowledge,\n"
                # TODO: This poetry line gets split when parsed because it contains a footnote
                "  but fools\n"
                "   despise wisdom and discipline."
            )
        ),
        (
            "Chapter break without a verse number is not skipped.",
            [
                {"book": "Psalms", "chapter": 131, "verse": '', "text": "", "type": "para", "marker": "b"},
                {"book": "Psalms", "chapter": 131, "verse": 1, "text": "My heart is not proud, O LORD,", "type": "para", "marker": "q1"},
                {"book": "Psalms", "chapter": 131, "verse": 1, "text": "my eyes are not haughty.", "type": "para", "marker": "q2"},
                {"book": "Psalms", "chapter": 131, "verse": 1, "text": "I do not aspire to great things", "type": "para", "marker": "q1"},
                {"book": "Psalms", "chapter": 131, "verse": 1, "text": "or matters too lofty for me.", "type": "para", "marker": "q2"},
                {"book": "Psalms", "chapter": 131, "verse": 2, "text": "Surely I have stilled and quieted my soul;", "type": "para", "marker": "q1"},
                {"book": "Psalms", "chapter": 131, "verse": 2, "text": "like a weaned child with his mother,", "type": "para", "marker": "q2"},
                {"book": "Psalms", "chapter": 131, "verse": 2, "text": "like a weaned child is my soul within me.", "type": "para", "marker": "q2"},
                {"book": "Psalms", "chapter": 131, "verse": 2, "text": "", "type": "para", "marker": "b"},
                {"book": "Psalms", "chapter": 131, "verse": 3, "text": "O Israel, put your hope in the LORD,", "type": "para", "marker": "q1"},
                {"book": "Psalms", "chapter": 131, "verse": 3, "text": "both now and forevermore.", "type": "para", "marker": "q2"},
            ],
            (
                "1 My heart is not proud, O LORD,\n"
                "  my eyes are not haughty.\n"
                "I do not aspire to great things\n"
                "  or matters too lofty for me.\n"
                "2 Surely I have stilled and quieted my soul;\n"
                "  like a weaned child with his mother,\n"
                "  like a weaned child is my soul within me.\n"
                "\n"
                "3 O Israel, put your hope in the LORD,\n"
                "  both now and forevermore."
            )
        ),
        (
            "Empty markup record is not skipped.",
            [
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "Instead, I hope to see you soon and speak with you face to face.", "type": "para", "marker": "m"},
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "", "type": "para", "marker": "m"},
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "", "type": "para", "marker": "b"},
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "Peace to you.", "type": "para", "marker": "m"},
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "", "type": "para", "marker": "b"},
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "The friends here send you greetings.", "type": "para", "marker": "m"},
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "", "type": "para", "marker": "b"},
                {"book": "3 John", "chapter": 1, "verse": 14, "text": "Greet each of our friends there by name.", "type": "para", "marker": "m"},
            ],
            (
                "14 Instead, I hope to see you soon and speak with you face to face.\n"
                "\n"
                "Peace to you.\n"
                "\n"
                "The friends here send you greetings.\n"
                "\n"
                "Greet each of our friends there by name."
            ),
        )
    ]
)    
def test_render_markup_verse_mumbers(msg, markup_records, rendered_passage):
    assert render_markup(markup_records, verse_numbers=True) == rendered_passage, msg
