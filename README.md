# Bible CLI: faster than flipping a page

## Installation
<!-- TODO: Publish app on pypi -->

Clone the repo to your machine:

```
git clone git@github.com:JStadnik619/bible-cli.git
```

Navigate to the repo's directory and install `biblecli` in your Python environment:

```
pip install .
```

## Usage

Look up a verse:

```
bible john 3 16
```

Look up a passage:

```
bible matthew 5 1-11
```

Look up a chapter:

```
bible psalm 117
```

Look up a book:

```
bible 3john
```

[BSB](https://berean.bible/index.html) is the default translation. Different translations can be selected via the `-t, --translation` flag:

<!-- TODO: Add more public domain translations -->

```
bible john 3 16 -t KJV
```

Line numbers can be toggled on using the `-n, --numbers` flag.

```
bible matthew 5 1-11 -n
```

The output format is specified using the `-f --format` flag (default: `txt` or plaintext).

```
bible matthew 5 1-11 -f md
```

### Book Abbreviations
<!-- TODO: Also map Bible versions to abbreviations? -->

Books can be referenced using the following titles and abbreviations (case-insensitive).

<!-- TODO: Map abbreviations to their usage in external Bibles/apps (eg. bible.com, MacArthur Study Bible) -->
<!-- TODO: Map books to abbreviations upon download from bible_databases -->
```
Genesis: genesis, gen, ge, gn
Exodus: exodus, ex, exod, exo
Leviticus: leviticus, lev, le, lv
Numbers: numbers, num, nu, nm, nb
Deuteronomy: deuteronomy, deut, de, dt
Joshua: joshua, josh, jos, jsh
Judges: judges, judg, jdg, jg, jdgs
Ruth: ruth, rth, ru
I Samuel: 1st samuel, 1 sam, 1sam, 1sm, 1sa, 1s, 1 samuel, 1samuel, 1st sam, first samuel, first sam
II Samuel: 2nd samuel, 2 sam, 2sam, 2sm, 2sa, 2s, 2 samuel, 2ndsam, 2nd sam, second samuel, second sam
I Kings: 1st kings, 1kings, 1 kings, 1kgs, 1 kgs, 1ki, 1k, 1stkgs, first kings, first kgs
II Kings: 2nd kings, 2kings, 2 kings, 2kgs, 2 kgs, 2ki, 2k, 2ndkgs, second kings, second kgs
I Chronicles: 1st chronicles, 1chronicles, 1 chronicles, 1chr, 1 chr, 1ch, 1stchr, 1st chr, first chronicles, first chr
II Chronicles: 2nd chronicles, 2chronicles, 2 chronicles, 2chr, 2 chr, 2ch, 2ndchr, 2nd chr, second chronicles, second chr
Ezra: ezra, ezr, ez
Nehemiah: nehemiah, neh, ne
Esther: esther, est, esth, es
Job: job, jb
Psalms: psalms, ps, psalm, pslm, psa, psm, pss
Proverbs: proverbs, prov, pro, prv, pr
Ecclesiastes: ecclesiastes, eccles, eccle, ecc, ec, qoh
Song of Solomon: song of solomon, song, song of songs, sos, so, canticle of canticles, canticles, cant
Isaiah: isaiah, isa, is
Jeremiah: jeremiah, jer, je, jr
Lamentations: lamentations, lam, la
Ezekiel: ezekiel, ezek, eze, ezk
Daniel: daniel, dan, da, dn
Hosea: hosea, hos, ho
Joel: joel, jl
Amos: amos, am
Obadiah: obadiah, obad, ob
Jonah: jonah, jnh, jon
Micah: micah, mic, mc
Nahum: nahum, nah, na
Habakkuk: habakkuk, hab, hb
Zephaniah: zephaniah, zeph, zep, zp
Haggai: haggai, hag, hg
Zechariah: zechariah, zech, zec, zc
Malachi: malachi, mal, ml
Matthew: matthew, matt, mt
Mark: mark, mrk, mar, mk, mr
Luke: luke, luk, lk
John: john, joh, jhn, jn
Acts: acts, act, ac
Romans: romans, rom, ro, rm
I Corinthians: 1 corinthians, 1corinthians, 1 cor, 1cor, 1 co, 1co, 1st corinthians, first corinthians
II Corinthians: 2 corinthians, 2corinthians, 2 cor, 2cor, 2 co, 2co, 2nd corinthians, second corinthians
Galatians: galatians, gal, ga
Ephesians: ephesians, eph, ephes
Philippians: philippians, phil, php, pp
Colossians: colossians, col, co
I Thessalonians: 1 thessalonians, 1thessalonians, 1 thess, 1thess, 1 thes, 1thes, 1 th, 1th, 1st thessalonians, 1st thess, first thessalonians, first thess
II Thessalonians: 2 thessalonians, 2thessalonians, 2 thess, 2thess, 2 thes, 2thes, 2 th, 2th, 2nd thessalonians, 2nd thess, second thessalonians, second thess
I Timothy: 1 timothy, 1timothy, 1 tim, 1tim, 1 ti, 1ti, 1st timothy, 1st tim, first timothy, first tim
II Timothy: 2 timothy, 2timothy, 2 tim, 2tim, 2 ti, 2ti, 2nd timothy, 2nd tim, second timothy, second tim
Titus: titus, tit, ti
Philemon: philemon, philem, phm, pm
Hebrews: hebrews, heb
James: james, jas, jm
I Peter: 1 peter, 1peter, 1 pet, 1pet, 1 pe, 1pe, 1 pt, 1pt, 1p, 1st peter, first peter
II Peter: 2 peter, 2peter, 2 pet, 2pet, 2 pe, 2pe, 2 pt, 2pt, 2p, 2nd peter, second peter
I John: 1 john, 1john, 1 jhn, 1jhn, 1 jn, 1jn, 1j, 1st john, first john
II John: 2 john, 2john, 2 jhn, 2jhn, 2 jn, 2jn, 2j, 2nd john, second john
III John: 3 john, 3john, 3 jhn, 3jhn, 3 jn, 3jn, 3j, 3rd john, third john
Jude: jude, jud, jd
Revelation of John: revelation, rev, re, the revelation
```

## Resources

<!-- TODO: Add subparser for downloading additional translations-->
[scrollmapper/bible_databases: Bible versions and cross-reference databases.](https://github.com/scrollmapper/bible_databases)

<!-- Users may not copy or download more than 500 verses of the ESV Bible -->
~~[ESV API | ESV.org](https://api.esv.org/)~~

## Similar Projects

[vitorpio/pybible-cli: Bible reference CLI application](https://github.com/vitorpio/pybible-cli)

[nehemiaharchives/bbl: Read, search Holy Bible in command line](https://github.com/nehemiaharchives/bbl)

[maxwelljens/bibel: Bible command line interface utility](https://github.com/maxwelljens/bibel)

[dtjm/bible: Command-line tool for reading the Bible](https://github.com/dtjm/bible)