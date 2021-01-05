This project creates jazz sheet music from guitar tabs, inspired by the style of Charlie Parker.  Currently alto saxophone is supported.

You'll need to install lilypond and add it to your path. If there are issues you could adjust line 174 to point at your lilypond executable, or manually run lilypond against the .ly files that are produced.

requirements:

python -m pip install requests

python -m pip install bs4

Usage: python process.py https://songster.com/taburl

This isn't suitable for orchestra use, but I sometimes use it as a starting point for riffs and key reference.

Depending on the tab, everything might be perfect :)

I included a few sample pdfs that were created with this program.
