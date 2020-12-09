#licensed under GPLv2
#version 0.1 10/20/2020 Rob Allen

#requirements for 1.0 release
#complete duration todo (see below)
#
#import ly
import os
import sys
import re
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("usage: python process.py url")
    print ("where url is a songster tab url like https://www.songsterr.com/a/wsa/metallica-orion-tab-s12369t1")
    sys.exit(0)

#infile
r = requests.get(sys.argv[1])
content = r.content
soup = BeautifulSoup(content,"html.parser")
inurl = soup.find_all("script",{"id":"state"})

outfile=(sys.argv[1]).split('/')[5]
outfile = open(outfile + '.ly','w')

duration=16
validDurations = [1,2,4,8,16]

def fixDuration(duration):
#todo: there's a time signature and duration issue which could be addressed
#by adding time signature calculations, lilypad interface complicates this
#current solution rounds the duration and defaults to a 16th note
#additionally we're not checking for dead notes which don't have a duration
#instead they're being passed as a high e 16th note.
    try:
        duration=duration.split(',')[1]
        duration = int(duration)
    except:
        duration=16
    if int(duration)>16:
        duration=16
    duration = closestDuration(validDurations, duration)
    return str(duration)+"\n"

def closestDuration(validDurations, duration):
    return validDurations[min(range(len(validDurations)), key = lambda i: abs(validDurations[i]-duration))]

#is = sharp
#es = flat

########
#todo "more elegant note calculation"
noteArray=["c","cis","d","dis","e","f","fis","g","gis","a","ais","b","c","cis","d","dis","e","f","fis","g","gis","a","ais","b","c","cis","d","dis","e","f","fis","g","gis","a","ais","b","c","cis","d","dis","e","f","fis","g","gis","a","ais","b"]
octaveNum=["'", "''", "'''"]
noteIdx = 0
octaveIdx = 0

#key adjustment for different instruments
instrument = "altoSax"
if instrument == "altoSax":
    keyAdjustment = 0 

def calcNoteRevised(string,fret,duration):
    global noteIdx
    global octaveIdx
    if string=="5":
        noteIdx=1+int(fret)
        if int(fret)>11:
            ocaveIdx=1
        else:
            octaveIdx=0
        return(noteArray[noteIdx]+octaveNum[octaveIdx]+fixDuration(duration))
    if string=="4":
        noteIdx=6+int(fret)
        if int(fret)>6:
            octaveIdx=1
        else:
            octaveIdx=0
        return(noteArray[noteIdx]+octaveNum[octaveIdx]+fixDuration(duration))
    if string=="3":
        noteIdx=11+int(fret)
        if int(fret)>12:
            octaveIdx=2
        elif int(fret)>0:
            octaveIdx=1
        else:
            octaveIdx=0
        return(noteArray[noteIdx]+octaveNum[octaveIdx]+fixDuration(duration))
    if string=="2":
        noteIdx=4+int(fret)
        if 7< int(fret) <11:
            octaveIdx=2
        else:
            octaveIdx=1
        return(noteArray[noteIdx]+octaveNum[octaveIdx]+fixDuration(duration))
    if string=="1":
        noteIdx=8+int(fret)
        if 3> int(fret)>8:
            octaveIdx=2
        else:
            octaveIdx=1
        return(noteArray[noteIdx]+octaveNum[octaveIdx]+fixDuration(duration))
    if string=="0":
        noteIdx=1+int(fret)
        if 10> int(fret)>15:
            octaveIdx=2
        else:
            octaveIdx=1
        return(noteArray[noteIdx]+octaveNum[octaveIdx]+fixDuration(duration))
    else:
        noteIdx=7
        octaveIdx=0
        return(noteArray[noteIdx]+octaveNum[octaveIdx]+fixDuration(duration))

########
#end "more elegant note calculation"
########




header = "{\n"
version = "\t\\version \"2.20.0\"\n"
time = "\t\\time 4/4\n"
clef ="\t\clef treble\n"
tail='}'    

notes=[]
finalNotes=[]
notesToWrite=[]

for x in inurl: 
    for y in x:
        split=y.split("{")
        for z in split:
            if "string" in z:
                finalNotes.append(z)
            if "rest" in z:
                finalNotes.append(z)

for x in finalNotes:
    if "\"string" in x:
        #print (x+"\n")
        string = (re.split(',|:', x))[1]
        #print(string)
        fret = (re.split(':|,|}', x))[3]
        #print(fret)
        if "duration" in x:
            duration = (re.split('\[|\]', x))[2]
            #print(duration)
        notesToWrite.append(calcNoteRevised(string,fret,duration))
    if "rest" in x:
        #print("rest")
        if "duration" in x:
            duration = (re.split('\[|\]', x))[2]
        finalNote=("r"+fixDuration(duration))
        notesToWrite.append(finalNote)

#for x in notesToWrite:
    #print(x)

outfile.write(header)
outfile.write(time)
outfile.write(clef)
for x in notesToWrite:
    outfile.write(x)
outfile.write(tail)
outfile.close()

#set this to your lilypond path, keep outfile.txt at the end
#example:
writer=os.system('lilypond --output=.\\outfiles\\ ' + outfile.name)
os.system('move '+ outfile.name +' lyfiles')
