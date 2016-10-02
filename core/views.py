from django.shortcuts import render, HttpResponse, redirect
import os
import numpy as np
import glob
import random
from random import randint
from django.db import models
import os, tempfile, zipfile
from pydub import AudioSegment
from django.utils.encoding import smart_str
import pydub
# Create your views here.
from core.models import Song, Vote
from .forms import ScoreForm



def download(request, filename):
    file_path = 'core/static/tuneFiles/'+filename+'.wav'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response



def index(request):
    if request.method == 'GET':
        oldSongs = glob.glob("core/static/tuneFiles/*.wav")
        songsNum = len(oldSongs)
        if(songsNum<3):
            a = AudioSegment.from_wav("core/notes/A.wav")
            b = AudioSegment.from_wav("core/notes/B.wav")
            c = AudioSegment.from_wav("core/notes/C.wav")
            d = AudioSegment.from_wav("core/notes/D.wav")
            e = AudioSegment.from_wav("core/notes/E.wav")
            f = AudioSegment.from_wav("core/notes/F.wav")
            g = AudioSegment.from_wav("core/notes/G.wav")
            asharp = AudioSegment.from_wav("core/notes/Asharp.wav")  # Bb
            dsharp = AudioSegment.from_wav("core/notes/Dsharp.wav")  # Eb
            csharp = AudioSegment.from_wav("core/notes/Csharp.wav")
            fsharp = AudioSegment.from_wav("core/notes/Fsharp.wav")
            gsharp = AudioSegment.from_wav("core/notes/Gsharp.wav")
            notesString = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'C#', 'D#', 'F#', 'G#', 'A#']
            notes = [a, b, c, d, e, f, g, csharp, dsharp, fsharp, gsharp, asharp]
            possTimes = [125, 250, 500, 750, 1000]


            def makeMelody(numNotes):
                #idx = np.random.choice(np.arange(len(notes)), numNotes, replace=True)
                #melody = notes[idx]
                #melodyString = notesString[idx]
                melody = []
                melodyString = []
                for x in range(0,numNotes):
                    choice = random.randint(0, len(notesString)-1)
                    melody.append(notes[choice])
                    melodyString.append(notesString[choice])
                return melody, melodyString

            def makeTimes(numNotes):
                times = []
                for x in range(0, numNotes):
                    times.append(random.choice(possTimes))
                return times

            def makeTimedMelody(melody, times):
                song = melody[0][:times[0]]
                for i in range(1, len(melody)):
                    song += melody[i][:times[i]]
                return song

            def makeFileName():
                oldSongs = glob.glob("core/static/tuneFiles/*.wav")
                songsNum = len(oldSongs)
                songcount = songsNum + 1
                return "tune%d.wav" %songcount

            def exportMelody(melody,fileName):
                melody.export("core/static/tuneFiles/%s" %fileName, format="wav")
                melody.export("crowdtunes/staticfiles/%s" % fileName, format="wav")

            # Create your views here.
            fileName = makeFileName()
            numNotes = 8
            melodyNotes,melodyString = makeMelody(numNotes)
            times = makeTimes(numNotes)
            timedMelody = makeTimedMelody(melodyNotes, times)
            exportMelody(timedMelody,fileName)
            fileName = fileName[:-4]
            form = ScoreForm()
            request.session['filename'] = fileName
            # Create new song object and save in database
            newsong = Song.objects.create_song(fileName,melodyString)
            newsong.save()
            return render(request, 'index.html', {'file_name':fileName, 'string':str(melodyString),'form':form})
        else:
            randsong = randint(1, songsNum)
            form = ScoreForm()
            request.session['filename'] = 'tune'+str(randsong)
            return render(request, 'index.html', {'file_name':'tune'+str(randsong),'string':'Previously generated song','form':form})
    else:
        form = ScoreForm(request.POST)
        if form.is_valid():
            filename_str = request.session['filename']
            # Find the Song object attached to this filename
            song = Song.objects.get(filename=filename_str)
            # Create vote
            rating = form.cleaned_data['chosenScore']
            newvote = Vote(score=rating, song=song)
            newvote.save()
            averageVote = (song.averageVote*song.dataPoints + song.score)/(song.dataPoints+1)
            song.dataPoints = song.dataPoints + 1
            song.save()
            return redirect('/')

def combined(request):
    def combine():
        all_songs = Song.objects.all().order_by('averageVote')
        chosen = [all_songs[len(all_songs)-1], all_songs[len(all_songs)-2], all_songs[len(all_songs)-3],
        all_songs[len(all_songs)-4]]
        return chosen

    def setMelody():
        a = AudioSegment.from_wav("core/notes/A.wav")
        b = AudioSegment.from_wav("core/notes/B.wav")
        c = AudioSegment.from_wav("core/notes/C.wav")
        d = AudioSegment.from_wav("core/notes/D.wav")
        e = AudioSegment.from_wav("core/notes/E.wav")
        f = AudioSegment.from_wav("core/notes/F.wav")
        g = AudioSegment.from_wav("core/notes/G.wav")
        asharp = AudioSegment.from_wav("core/notes/Asharp.wav")  # Bb
        dsharp = AudioSegment.from_wav("core/notes/Dsharp.wav")  # Eb
        csharp = AudioSegment.from_wav("core/notes/Csharp.wav")
        fsharp = AudioSegment.from_wav("core/notes/Fsharp.wav")
        gsharp = AudioSegment.from_wav("core/notes/Gsharp.wav")
        notesString = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'C#', 'D#', 'F#', 'G#', 'A#']
        notes = [a, b, c, d, e, f, g, csharp, dsharp, fsharp, gsharp, asharp]
        possTimes = [125, 250, 500, 750, 1000]
        melody = []
        for x in chosen:
            melody.append(chosen[i].



        melody = []
        melodyString = []
        for x in range(0, numNotes):
            choice = random.randint(0, len(notesString) - 1)
            melody.append(notes[choice])
            melodyString.append(notesString[choice])
        return melody, melodyString


    return render(request, 'combined.html', {'message':'hello!'})
