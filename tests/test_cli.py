import pytest
import sys

from berea.cli import main, CLIConfig
from berea.utils import get_downloaded_translations


@pytest.mark.parametrize(
    "msg, args, output", 
    [
        (
            "Printing a single verse failed",
            ['john', '3', '16'],
            (
                "For God so loved the world that He gave His one and only Son, that everyone\n"
                "who believes in Him shall not perish but have eternal life. "
            )
        ),
        (
            "Printing multiple verses failed",
            ['john', '3', '16-18'],
            (
                "For God so loved the world that He gave His one and only Son, that everyone\n"
                "who believes in Him shall not perish but have eternal life. For God did not\n"
                "send His Son into the world to condemn the world, but to save the world\n"
                "through Him. Whoever believes in Him is not condemned, but whoever does not\n"
                "believe has already been condemned, because he has not believed in the name of\n"
                "God’s one and only Son. "
            )
        ),
        (
            "Printing multiple verses with verse numbers failed",
            ['john', '3', '16-18', '-n'],
            (
                "16 For God so loved the world that He gave His one and only Son, that everyone\n"
                "who believes in Him shall not perish but have eternal life. 17 For God did not\n"
                "send His Son into the world to condemn the world, but to save the world\n"
                "through Him. 18 Whoever believes in Him is not condemned, but whoever does not\n"
                "believe has already been condemned, because he has not believed in the name of\n"
                "God’s one and only Son. "
            )
        ),
        (
            "Printing a chapter failed",
            ['psa', '117'],
            (
                "Praise the LORD, all you nations! Extol Him, all you peoples! For great is His\n"
                "loving devotion toward us, and the faithfulness of the LORD endures forever.  \n"
                "Hallelujah! "
            )
        ),
        (
            "Printing a chapter with verse numbers failed",
            ['psa', '117', '-n'],
            (
                "1 Praise the LORD, all you nations! Extol Him, all you peoples! 2 For great is\n"
                "His loving devotion toward us, and the faithfulness of the LORD endures\n"
                "forever.   Hallelujah! "
            )
        ),
        (
            "Printing a book failed",
            ['3john'],
            (
                "The elder,  To the beloved Gaius, whom I love in the truth: Beloved, I pray\n"
                "that in every way you may prosper and enjoy good health, as your soul also\n"
                "prospers. For I was overjoyed when the brothers came and testified about your\n"
                "devotion to the truth, in which you continue to walk. I have no greater joy\n"
                "than to hear that my children are walking in the truth. Beloved, you are\n"
                "faithful in what you are doing for the brothers, and especially since they are\n"
                "strangers to you. They have testified to the church about your love. You will\n"
                "do well to send them on their way in a manner worthy of God. For they went out\n"
                "on behalf of the Name, accepting nothing from the Gentiles. Therefore we ought\n"
                "to support such men, so that we may be fellow workers for the truth. I have\n"
                "written to the church about this, but Diotrephes, who loves to be first, will\n"
                "not accept our instruction. So if I come, I will call attention to his\n"
                "malicious slander against us. And unsatisfied with that, he refuses to welcome\n"
                "the brothers and forbids those who want to do so, even putting them out of the\n"
                "church. Beloved, do not imitate what is evil, but what is good. The one who\n"
                "does good is of God; the one who does evil has not seen God. Demetrius has\n"
                "received a good testimony from everyone, and from the truth itself. We also\n"
                "testify for him, and you know that our testimony is true. I have many things\n"
                "to write to you, but I would prefer not to do so with pen and ink. Instead, I\n"
                "hope to see you soon and speak with you face to face.  Peace to you.  The\n"
                "friends here send you greetings.  Greet each of our friends there by name. "
            )
        ),
        (
            "Printing a book with verse numbers failed",
            ['3john', '-n'],
            (
                "1 The elder,  To the beloved Gaius, whom I love in the truth: 2 Beloved, I\n"
                "pray that in every way you may prosper and enjoy good health, as your soul\n"
                "also prospers. 3 For I was overjoyed when the brothers came and testified\n"
                "about your devotion to the truth, in which you continue to walk. 4 I have no\n"
                "greater joy than to hear that my children are walking in the truth. 5 Beloved,\n"
                "you are faithful in what you are doing for the brothers, and especially since\n"
                "they are strangers to you. 6 They have testified to the church about your\n"
                "love. You will do well to send them on their way in a manner worthy of God. 7\n"
                "For they went out on behalf of the Name, accepting nothing from the Gentiles.\n"
                "8 Therefore we ought to support such men, so that we may be fellow workers for\n"
                "the truth. 9 I have written to the church about this, but Diotrephes, who\n"
                "loves to be first, will not accept our instruction. 10 So if I come, I will\n"
                "call attention to his malicious slander against us. And unsatisfied with that,\n"
                "he refuses to welcome the brothers and forbids those who want to do so, even\n"
                "putting them out of the church. 11 Beloved, do not imitate what is evil, but\n"
                "what is good. The one who does good is of God; the one who does evil has not\n"
                "seen God. 12 Demetrius has received a good testimony from everyone, and from\n"
                "the truth itself. We also testify for him, and you know that our testimony is\n"
                "true. 13 I have many things to write to you, but I would prefer not to do so\n"
                "with pen and ink. 14 Instead, I hope to see you soon and speak with you face\n"
                "to face.  Peace to you.  The friends here send you greetings.  Greet each of\n"
                "our friends there by name. "
            )
        ),
        (
            "Printing a different translation failed",
            ['john', '3', '16', '-t', 'KJV'],
            (
                "For God so loved the world, that he gave his only begotten Son, that whosoever\n"
                "believeth in him should not perish, but have everlasting life. "
            )    
        ),
        (
            "Creating a Markdown excerpt failed",
            ['john', '3', '16', '-f', 'md'],
            (
                "###\n\n"
                "______________________________________________________________________\n\n"
                "For God so loved the world that He gave His one and only Son, that everyone\n"
                "who believes in Him shall not perish but have eternal life. \n"
                "([John 3:16 BSB](https://www.stepbible.org/?q=version=BSB@reference=john.3.16&options=NVHUG))\n\n"
                "______________________________________________________________________"
            )
        ),
        (
            "Creating a Markdown excerpt for multiple verses failed",
            ['john', '3', '16-18', '-f', 'md'],
            (
                "###\n\n"
                "______________________________________________________________________\n\n"
                "For God so loved the world that He gave His one and only Son, that everyone\n"
                "who believes in Him shall not perish but have eternal life. For God did not\n"
                "send His Son into the world to condemn the world, but to save the world\n"
                "through Him. Whoever believes in Him is not condemned, but whoever does not\n"
                "believe has already been condemned, because he has not believed in the name of\n"
                "God’s one and only Son. \n"
                "([John 3:16-18 BSB](https://www.stepbible.org/?q=version=BSB@reference=john.3.16-john.3.18&options=NVHUG))\n\n"
                "______________________________________________________________________"
            )
        ),
        (
            "Creating a Markdown excerpt with verse numbers failed",
            ['john', '3', '16-18', '-f', 'md', '-n'],
            (
                "###\n\n"
                "______________________________________________________________________\n\n"
                "<sup>16</sup> For God so loved the world that He gave His one and only Son,\n"
                "that everyone who believes in Him shall not perish but have eternal life.\n"
                "<sup>17</sup> For God did not send His Son into the world to condemn the\n"
                "world, but to save the world through Him. <sup>18</sup> Whoever believes in\n"
                "Him is not condemned, but whoever does not believe has already been condemned,\n"
                "because he has not believed in the name of God’s one and only Son. \n"
                "([John 3:16-18 BSB](https://www.stepbible.org/?q=version=BSB@reference=john.3.16-john.3.18&options=NVHUG))\n\n"
                "______________________________________________________________________"
            )
        ),
        # The BSB contains empty verses for cross-references to verses present
        # in some manuscripts
        (
            "Skipping empty verses failed",
            ['mark', '9', '43-47', '-n'],
            (
                "43 If your hand causes you to sin, cut it off. It is better for you to enter\n"
                "life crippled than to have two hands and go into hell, into the unquenchable\n"
                "fire. 45 If your foot causes you to sin, cut it off. It is better for you to\n"
                "enter life lame than to have two feet and be thrown into hell. 47 And if your\n"
                "eye causes you to sin, pluck it out. It is better for you to enter the kingdom\n"
                "of God with one eye than to have two eyes and be thrown into hell, "
            )
        ),
        # Error path tests
        (
            "Failed to validate book input",
            ['silmarillion'],
            "Invalid input book='silmarillion'."
        ),
        (
            "Failed to validate chapter input",
            ['acts', '29'],
            "Invalid chapter: Acts 29."
        ),
        (
            "Failed to validate verse input",
            ['acts', '28', '100'],
            "Invalid verse: Acts 28:100."
        ),
        (
            "Failed to validate verse input for multiple verses",
            ['acts', '28', '100-200'],
            "Invalid verses: Acts 28:100-200."
        ),
    ]
)
def test_reference(monkeypatch, capsys, msg, args, output):
    args.insert(0, 'bible')
    monkeypatch.setattr(sys, 'argv', args)
    
    main()
    
    captured = capsys.readouterr()
    assert captured.out == output + '\n', msg


def test_delete(monkeypatch, capsys):
    default_translation = CLIConfig.get_default_translation()
    monkeypatch.setattr(sys, 'argv', ['bible', 'delete', default_translation])
    main()
    
    assert not pytest.translation_exists(default_translation)
    captured = capsys.readouterr()
    assert captured.out == f"Deleted translation '{default_translation}'.\n"
    
    downloaded_translations = get_downloaded_translations()
    
    msg = "Failed to update config after deleting default translation"
    new_default_translation = CLIConfig.get_default_translation()
    assert new_default_translation == downloaded_translations[0], msg
    
    # Delete remaining translations
    for translation in downloaded_translations:
        monkeypatch.setattr(sys, 'argv', ['bible', 'delete', translation])
        main()
    
        assert not pytest.translation_exists(translation)
        captured = capsys.readouterr()
        assert captured.out == f"Deleted translation '{translation}'.\n"
    
    msg = "Failed to update config if no other translation is downloaded"
    assert CLIConfig.get_default_translation() == 'None', msg


def test_download_sets_default_translation(monkeypatch):
    # Delete remaining translations if any exist
    downloaded_translations = get_downloaded_translations()
    if downloaded_translations:
        for translation in downloaded_translations:
            monkeypatch.setattr(sys, 'argv', ['bible', 'delete', translation])
            main()
    
    monkeypatch.setattr(sys, 'argv', ['bible', 'download', 'BSB'])
    main()
    
    msg = "Failed to set first download as the default translation"
    assert CLIConfig.get_default_translation() == 'BSB', msg


@pytest.mark.parametrize(
    "translation",
    [
        ('KJV'),
        ('BSB'),
        ('LEB'),
        ('RLT'),        
        ('UKJV'),        
    ]
)
def test_download(monkeypatch, capsys, translation):
    if translation in get_downloaded_translations():
        monkeypatch.setattr(sys, 'argv', ['bible', 'delete', translation])
        main()
    
    args = ['bible', 'download']
    args.append(translation)
    monkeypatch.setattr(sys, 'argv', args)
    
    main()
    
    captured = capsys.readouterr()
    assert all(s in captured.out for s in ['Downloaded:', f'{translation}.db'])
    
    assert pytest.translation_exists(translation)


def test_download_error(monkeypatch, capsys):
    # The ESV is not public domain
    translation = 'ESV'
    
    args = ['bible', 'download']
    args.append(translation)
    monkeypatch.setattr(sys, 'argv', args)
    
    main()
    
    output = (
        f"Translation '{translation}' does not exist.\n"
        f"Check the following link for available translations:\n"
        "https://github.com/jstadnik619/bible_databases?tab=readme-ov-file#available-translations-140"
    )
    
    captured = capsys.readouterr()
    assert captured.out == output + '\n'
    assert not pytest.translation_exists(translation)


@pytest.mark.parametrize(
    "msg, args, output",
    [
        (
            "Searching an exact phrase with a single occurrence failed",
            ['"rescue my soul"', '-t', 'BSB'],
            (
                "1 occurrences of '\"rescue my soul\"' in the BSB Bible:\n"
                "___\n\n"
                "Psalms 35:17:\n"
                "How long, O Lord, will You look on? \x1b[1mRescue my soul\x1b[0m from their ravages, my precious life from these lions. \n"
                "___\n"
            )
        ),
        (
            "Searching an exact phrase with multiple occurrences failed",
            ['"sheep gate"', '-t', 'BSB'],
            (
                "4 occurrences of '\"sheep gate\"' in the BSB Bible:\n"
                "___\n\n"
                "Nehemiah 3:1:\n"
                "At the \x1b[1mSheep Gate\x1b[0m, Eliashib the high priest and his fellow priests began rebuilding. They dedicated it and installed its doors. After building as far as the Tower of the Hundred and the Tower of Hananel, they dedicated the wall. \n"
                "___\n\n"
                "Nehemiah 3:32:\n"
                "And between the upper room above the corner and the \x1b[1mSheep Gate\x1b[0m, the goldsmiths and merchants made repairs. \n"
                "___\n\n"
                "Nehemiah 12:39:\n"
                "over the Gate of Ephraim, the Jeshanah Gate, the Fish Gate, the Tower of Hananel, and the Tower of the Hundred, as far as the \x1b[1mSheep Gate\x1b[0m. And they stopped at the Gate of the Guard. \n"
                "___\n\n"
                "John 5:2:\n"
                "Now there is in Jerusalem near the \x1b[1mSheep Gate\x1b[0m a pool with five covered colonnades, which in Hebrew is called Bethesda. \n"
                "___\n"
            )
        ),
        (
            "Searching an exact phrase in the Old Testament failed",
            ['"holy spirit"', '-OT', '-t', 'BSB'],
            (
                "3 occurrences of '\"holy spirit\"' in the Old Testament (BSB):\n"
                "___\n\n"
                "Psalms 51:11:\n"
                "Cast me not away from Your presence; take not Your \x1b[1mHoly Spirit\x1b[0m from me. \n"
                "___\n\n"
                "Isaiah 63:10:\n"
                "But they rebelled and grieved His \x1b[1mHoly Spirit\x1b[0m. So He turned and became their enemy, and He Himself fought against them.   \n"
                "___\n\n"
                "Isaiah 63:11:\n"
                "Then His people remembered the days of old, the days of Moses. Where is He who brought them through the sea with the shepherds of His flock? Where is the One who set His \x1b[1mHoly Spirit\x1b[0m among them, \n"
                "___\n"
            )
        ),
        (
            "Searching an exact phrase in the New Testament failed",
            ['"justified by faith"', '-NT', '-t', 'BSB'],
            (
                "3 occurrences of '\"justified by faith\"' in the New Testament (BSB):\n"
                "___\n\n"
                "Romans 3:28:\n"
                "For we maintain that a man is \x1b[1mjustified by faith\x1b[0m apart from works of the law. \n"
                "___\n\n"
                "Galatians 2:16:\n"
                "know that a man is not justified by works of the law, but by faith in Jesus Christ. So we, too, have believed in Christ Jesus, that we may be \x1b[1mjustified by faith\x1b[0m in Christ and not by works of the law, because by works of the law no one will be justified. \n"
                "___\n\n"
                "Galatians 3:24:\n"
                "So the law became our guardian to lead us to Christ, that we might be \x1b[1mjustified by faith\x1b[0m. \n"
                "___\n"
            )
        ),
        (
            "Searching a phrase in a book failed",
            ['"lying spirit"', '2chr', '-t', 'BSB'],
            (
                "2 occurrences of '\"lying spirit\"' in II Chronicles (BSB):\n"
                "___\n\n"
                "II Chronicles 18:21:\n"
                "And he replied, ‘I will go out and be a \x1b[1mlying spirit\x1b[0m in the mouths of all his prophets.’  ‘You will surely entice him and prevail,’ said the LORD. ‘Go and do it.’ \n"
                "___\n\n"
                "II Chronicles 18:22:\n"
                "So you see, the LORD has put a \x1b[1mlying spirit\x1b[0m in the mouths of these prophets of yours, and the LORD has pronounced disaster against you.” \n"
                "___\n"
            )
        ),
        (
            "Searching a phrase in a chapter failed",
            ['lampstands', 'rev', '1', '-t', 'BSB'],
            (
                "3 occurrences of 'lampstands' in Revelation of John 1 (BSB):\n"
                "___\n\n"
                "Revelation of John 1:12:\n"
                "Then I turned to see the voice that was speaking with me. And having turned, I saw seven golden \x1b[1mlampstands\x1b[0m, \n"
                "___\n\n"
                "Revelation of John 1:13:\n"
                "and among the \x1b[1mlampstands\x1b[0m was One like the Son of Man, dressed in a long robe, with a golden sash around His chest. \n"
                "___\n\n"
                "Revelation of John 1:20:\n"
                "This is the mystery of the seven stars you saw in My right hand and of the seven golden \x1b[1mlampstands\x1b[0m: The seven stars are the angels of the seven churches, and the seven \x1b[1mlampstands\x1b[0m are the seven churches. \n"
                "___\n"
            )
        ),
        (
            "Searching a tokenized phrase in the Bible failed",
            ['justified faith', '-t', 'BSB'],
            (
                "6 occurrences of 'justified faith' in the BSB Bible:\n"
                "___\n\n"
                "Romans 3:28:\n"
                "For we maintain that a man is \x1b[1mjustified\x1b[0m by \x1b[1mfaith\x1b[0m apart from works of the law. \n"
                "___\n\n"
                "Romans 5:1:\n"
                "Therefore, since we have been \x1b[1mjustified\x1b[0m through \x1b[1mfaith\x1b[0m, we have peace with God through our Lord Jesus Christ, \n"
                "___\n\n"
                "Galatians 2:16:\n"
                "know that a man is not \x1b[1mjustified\x1b[0m by works of the law, but by \x1b[1mfaith\x1b[0m in Jesus Christ. So we, too, have believed in Christ Jesus, that we may be \x1b[1mjustified\x1b[0m by \x1b[1mfaith\x1b[0m in Christ and not by works of the law, because by works of the law no one will be \x1b[1mjustified\x1b[0m. \n"
                "___\n\n"
                "Galatians 3:11:\n"
                "Now it is clear that no one is \x1b[1mjustified\x1b[0m before God by the law, because, “The righteous will live by \x1b[1mfaith\x1b[0m.” \n"
                "___\n\n"
                "Galatians 3:24:\n"
                "So the law became our guardian to lead us to Christ, that we might be \x1b[1mjustified\x1b[0m by \x1b[1mfaith\x1b[0m. \n"
                "___\n\n"
                "James 2:24:\n"
                "As you can see, a man is \x1b[1mjustified\x1b[0m by his deeds and not by \x1b[1mfaith\x1b[0m alone. \n"
                "___\n"
            )
        ),
        (
            "Searching a tokenized phrase in the Old Testament failed",
            ['serpent dust', '-OT', '-t', 'BSB'],
            (
                "2 occurrences of 'serpent dust' in the Old Testament (BSB):\n"
                "___\n\n"
                "Genesis 3:14:\n"
                " So the LORD God said to the \x1b[1mserpent\x1b[0m:  “Because you have done this, cursed are you above all livestock and every beast of the field! On your belly will you go, and \x1b[1mdust\x1b[0m you will eat, all the days of your life. \n"
                "___\n\n"
                "Isaiah 65:25:\n"
                "The wolf and the lamb will feed together, and the lion will eat straw like the ox, but the food of the \x1b[1mserpent\x1b[0m will be \x1b[1mdust\x1b[0m. They will neither harm nor destroy on all My holy mountain,” says the LORD.   \n"
                "___\n"
            )
        ),
        (
            "Searching a tokenized phrase in the New Testament failed",
            ['justified by faith', '-NT', '-t', 'BSB'],
            (
                "5 occurrences of 'justified by faith' in the New Testament (BSB):\n"
                "___\n\n"
                "Romans 3:28:\n"
                "For we maintain that a man is \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m apart from works of the law. \n"
                "___\n\n"
                "Galatians 2:16:\n"
                "know that a man is not \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m works of the law, but \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m in Jesus Christ. So we, too, have believed in Christ Jesus, that we may be \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m in Christ and not \x1b[1mby\x1b[0m works of the law, because \x1b[1mby\x1b[0m works of the law no one will be \x1b[1mjustified\x1b[0m. \n"
                "___\n\n"
                "Galatians 3:11:\n"
                "Now it is clear that no one is \x1b[1mjustified\x1b[0m before God \x1b[1mby\x1b[0m the law, because, “The righteous will live \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m.” \n"
                "___\n\n"
                "Galatians 3:24:\n"
                "So the law became our guardian to lead us to Christ, that we might be \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m. \n"
                "___\n\n"
                "James 2:24:\n"
                "As you can see, a man is \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m his deeds and not \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m alone. \n"
                "___\n"
            )
        ),
        (
            "Searching a tokenized phrase in a book failed",
            ['justified by faith', 'gal', '-t', 'BSB'],
            (
                "3 occurrences of 'justified by faith' in Galatians (BSB):\n"
                "___\n\n"
                "Galatians 2:16:\n"
                "know that a man is not \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m works of the law, but \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m in Jesus Christ. So we, too, have believed in Christ Jesus, that we may be \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m in Christ and not \x1b[1mby\x1b[0m works of the law, because \x1b[1mby\x1b[0m works of the law no one will be \x1b[1mjustified\x1b[0m. \n"
                "___\n\n"
                "Galatians 3:11:\n"
                "Now it is clear that no one is \x1b[1mjustified\x1b[0m before God \x1b[1mby\x1b[0m the law, because, “The righteous will live \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m.” \n"
                "___\n\n"
                "Galatians 3:24:\n"
                "So the law became our guardian to lead us to Christ, that we might be \x1b[1mjustified\x1b[0m \x1b[1mby\x1b[0m \x1b[1mfaith\x1b[0m. \n"
                "___\n"
            )
        ),
        (
            "Searching a tokenized phrase in a chapter failed",
            ['one man', 'rev', '1', '-t', 'BSB'],
            (
                "1 occurrences of 'one man' in Revelation of John 1 (BSB):\n"
                "___\n\n"
                "Revelation of John 1:13:\n"
                "and among the lampstands was \x1b[1mOne\x1b[0m like the Son of \x1b[1mMan\x1b[0m, dressed in a long robe, with a golden sash around His chest. \n"
                "___\n"
            )
        ),
        (
            "Searching a prefix in a chapter failed",
            ['justif*', 'rom', '5', '-t', 'BSB'],
            (
                "4 occurrences of 'justif*' in Romans 5 (BSB):\n"
                "___\n\n"
                "Romans 5:1:\n"
                "Therefore, since we have been \x1b[1mjustified\x1b[0m through faith, we have peace with God through our Lord Jesus Christ, \n"
                "___\n\n"
                "Romans 5:9:\n"
                "Therefore, since we have now been \x1b[1mjustified\x1b[0m by His blood, how much more shall we be saved from wrath through Him! \n"
                "___\n\n"
                "Romans 5:16:\n"
                "Again, the gift is not like the result of the one man’s sin: The judgment that followed one sin brought condemnation, but the gift that followed many trespasses brought \x1b[1mjustification\x1b[0m. \n"
                "___\n\n"
                "Romans 5:18:\n"
                "So then, just as one trespass brought condemnation for all men, so also one act of righteousness brought \x1b[1mjustification\x1b[0m and life for all men. \n"
                "___\n"
            )
        ),
        (
            "Searching a phrase with boolean operators (NOT) in a book failed",
            ['mercy NOT seat', 'exo', '-t', 'BSB'],
            (
                "1 occurrences of 'mercy NOT seat' in Exodus (BSB):\n"
                "___\n\n"
                "Exodus 33:19:\n"
                "“I will cause all My goodness to pass before you,” the LORD replied, “and I will proclaim My name—the LORD—in your presence. I will have \x1b[1mmercy\x1b[0m on whom I have \x1b[1mmercy\x1b[0m, and I will have compassion on whom I have compassion.” \n"
                "___\n"
            )
        ),
        (
            "Searching a phrase with boolean operators "
            "(NOT, OR) in a book failed",
            ['james NOT (alphaeus OR john)', 'acts', '-t', 'BSB'],
            (
                "3 occurrences of 'james NOT (alphaeus OR john)' in Acts (BSB):\n"
                "___\n\n"
                "Acts 12:17:\n"
                "Peter motioned with his hand for silence, and he described how the Lord had brought him out of the prison. “Send word to \x1b[1mJames\x1b[0m and to the brothers,” he said, and he left for another place. \n"
                "___\n\n"
                "Acts 15:13:\n"
                "When they had finished speaking, \x1b[1mJames\x1b[0m declared, “Brothers, listen to me! \n"
                "___\n\n"
                "Acts 21:18:\n"
                "The next day Paul went in with us to see \x1b[1mJames\x1b[0m, and all the elders were present. \n"
                "___\n"
            )
        ),
        # TODO: Is suffix searching possible with FTS5 or even useful?
        # Error path tests
        (
            "Searching a phrase in a chapter with the New Testament flag should be invalid",
            ['lampstands', 'rev', '1', '-NT'],
            (
                "Invalid search: cannot search a chapter with the '-NT, --new_testament' flag."
            )
        ),
        (
            "Searching a phrase in a book with the Old Testament flag should be invalid",
            ['holy spirit', 'isa', '-OT'],
            (
                "Invalid search: cannot search a book with the '-OT, --old_testament' flag."
            )
        ),
    ]
)
def test_search(monkeypatch, capsys, msg, args, output):
    args = ['bible', 'search'] +  args
    monkeypatch.setattr(sys, 'argv', args)
    
    main()
    
    captured = capsys.readouterr()
    assert captured.out == output + '\n', msg


@pytest.mark.parametrize(
    "translation",
    [
        ('KJV'),
        ('LEB'),
        ('RLT'),        
        ('UKJV'),      
        ('BSB'), 
    ]
)
def test_config_default_translation(monkeypatch, capsys, translation):
    args = ['bible', 'config', 'translation', translation]
    monkeypatch.setattr(sys, 'argv', args)
    
    main()
    
    captured = capsys.readouterr()
    assert captured.out == "Default translation updated.\n"
    
    msg = "Setting the default translation failed"
    assert CLIConfig.get_default_translation() == translation, msg
