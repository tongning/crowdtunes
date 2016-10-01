from django.shortcuts import render

import os
import numpy as np
import random
from pydub import AudioSegment
import pydub

a = AudioSegment.from_wav("notes/A.wav")
b = AudioSegment.from_wav("notes/B.wav")
c = AudioSegment.from_wav("notes/C.wav")
d = AudioSegment.from_wav("notes/D.wav")
e = AudioSegment.from_wav("notes/E.wav")
f = AudioSegment.from_wav("notes/F.wav")
g = AudioSegment.from_wav("notes/G.wav")
asharp = AudioSegment.from_wav("notes/Asharp.wav")  # Bb
dsharp = AudioSegment.from_wav("notes/Dsharp.wav")  # Eb
csharp = AudioSegment.from_wav("notes/Csharp.wav")
fsharp = AudioSegment.from_wav("notes/Fsharp.wav")
gsharp = AudioSegment.from_wav("notes/Gsharp.wav")
notesString = ['A','B','C','D','E','F','G','Csharp','Dsharp','Fsharp','Gsharp','Asharp']
notes = [a, b, c, d, e, f, g, csharp, dsharp, fsharp, gsharp, asharp]
possTimes = [125, 250, 500, 750, 1000]

def makeMelody(numNotes):
    melody,melodyString = []
    idx = np.random.choice(np.arange(notes), numNotes, replace=True)
    melody = notes[idx]
    melodyString = notesString[idx]
    return melody, melodyString

def makeTimes(numNotes):
    times = []
    for x in xrange(0, numNotes):
        times.append(random.choice(possTimes))
    return times

def makeTimedMelody(melody, times):
    song = melody[0][:times[0]]
    for i in xrange(1, len(melody)):
        song += melody[i][:times[i]]
    return song

def exportMelody(melody):
    import glob
    oldSongs = glob.glob("../crowdtunes/staticfiles/tuneFiles/*.wav")
    songsNum = len(oldSongs)
    songcount = songsNum + 1
    melody.export("../crowdtunes/staticfiles/tuneFiles/tune%d.wav" % songcount, format="wav")

# Create your views here.
def index(request):
    numNotes = 8
    melodyNotes, melodyString = makeMelody(numNotes)
    times = makeTimes(numNotes)
    timedMelody = makeTimedMelody(melodyNotes, times)
    exportMelody(timedMelody)

    return render(request, 'index.html' )