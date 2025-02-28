import pytest
import sys

from biblecli.cli import main


@pytest.mark.parametrize(
    "msg, args, output", 
    [
        (
            "Reading a single verse failed",
            ['john', '3', '16'],
            (
                "For God so loved the world that He gave His one and only Son, that everyone\n"
                "who believes in Him shall not perish but have eternal life. "
            )
        ),
        (
            "Reading a multiple verses failed",
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
            "Reading a chapter failed",
            ['psa', '117'],
            (
                "Praise the LORD, all you nations! Extol Him, all you peoples! For great is His\n"
                "loving devotion toward us, and the faithfulness of the LORD endures forever.  \n"
                "Hallelujah! "
            )
        ),
        (
            "Reading a book failed",
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
            "Creating a Markdown excerpt failed",
            ['john', '3', '16', '-f', 'md'],
            (
                "###\n\n"
                "______________________________________________________________________\n\n"
                "For God so loved the world that He gave His one and only Son, that everyone\n"
                "who believes in Him shall not perish but have eternal life. \n"
                "([John 3:16 BSB]())\n\n"
                "______________________________________________________________________"
            )
        ),
    ]
)
def test_main(monkeypatch, capsys, msg, args, output):
    args.insert(0, 'bible')
    monkeypatch.setattr(sys, 'argv', args)
    
    main()
    
    captured = capsys.readouterr()
    assert captured.out == output + '\n', msg
