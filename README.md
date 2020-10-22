This project takes guitar tabs as input and transposes them into sheet music.  Currently alto saxophone is supported.  It's farily simple to edit the key to accomodate a different instrument in the program, but not accessible through an external interface yet.

dependencies: lilypond

usage: python tabs_to_sax0.1.py inFileName.ext

where inFileName.ext is a tab file you've saved from songster (use wget or save source).

current version requires to you change this line (line 162) to point at your lilypond executable, alternatively you could run lilypond using the outfile as source:

#example writer=os.system('C:\\\\Users\\\\Herman Li\\\\Documents\\\\LilyPond\\\usr\\\\bin\\\\lilypond outfile.txt')

writer=os.system('lilypond '+sys.argv[1]+'_outfile.txt')

There are some issues with chords/slides and some note combinations which will be worked on during a later release version.

There are issues with note durations - this isn't suitable for orchestra use, but I sometimes use it as a starting point and key reference.

Depending on the tab, everything might be perfect :)

I included a few sample pdfs that were created with this program.
