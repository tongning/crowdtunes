from django.shortcuts import render, HttpResponse,redirect, HttpResponseRedirect
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
from .forms import ScoreForm, NotesForm


givenNotes = []
def download(request, filename):
    file_path = 'core/static/tuneFiles/'+filename+'.wav'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
def downloadSong(request, filename):
    file_path = 'core/static/combinedFiles/'+filename+'.wav'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

def createYourOwn(request): #DOESNT WORK YET
    global givenNotes
    if request.method == 'GET':
        form = NotesForm()
        return render(request, 'createYourOwn.html', {'form': form})
    else:
        form = NotesForm(request.POST)
        if form.is_valid():
            notesStr = form.cleaned_data['notes']
            notesStr = notesStr.upper()
            givenNotes = notesStr.split(" ")
            return redirect('/')

def about(request):
    return render(request, 'about.html')

def index(request):
    global givenNotes
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
    notesString = ['A', 'A#', 'B', 'C', 'C#''D', 'D#','E', 'F', 'F#','G', 'G#']
    notes = [a,  asharp , b, c, csharp , d , dsharp , e , f, fsharp, g, gsharp]
    possTimes = [125, 250, 500, 750, 1000]
    oldSongs = glob.glob("core/static/tuneFiles/*.wav")
    songsNum = len(oldSongs)

    def makeMelody(numNotes):
        melody = []
        melodyString = []
        for x in range(0, numNotes):
            choice = random.randint(-3, len(notesString)+2)
            try:
                if choice >= len(notesString):
                    choice = random.randint(melody[x-1-random.randint(1,2)])
                elif (choice < 0):
                    choice = random.randint(melody[x-1+random.randint(1,2)])
            except:
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
        return "tune%d.wav" % songcount

    def exportMelody(melody, fileName):
        melody.export("core/static/tuneFiles/%s" % fileName, format="wav")
        melody.export("crowdtunes/staticfiles/%s" % fileName, format="wav")

    if request.method == 'GET':
        if givenNotes!=[]:
            melody = []
            for i in range(0,len(givenNotes)):
                ind = notesString.index(givenNotes[i])
                melody.append(notes[ind])
            times = makeTimes(len(melody)) #make random times for now
            timedMelody = makeTimedMelody(melody,times)
            fileName = makeFileName()
            form = ScoreForm()
            exportMelody(timedMelody,fileName)
            givenNotesStr = str(givenNotes)
            givenNotes = []
            return render(request, 'index.html', {'file_name': fileName[:-4], 'string': givenNotesStr, 'form': form})
        elif songsNum<60:
            fileName = makeFileName()
            numNotes = 8
            melodyNotes,melodyString = makeMelody(numNotes)
            times = makeTimes(numNotes)
            timedMelody = makeTimedMelody(melodyNotes, times)
            exportMelody(timedMelody,fileName)
            fileName = fileName[:-4] #omit .wav
            form = ScoreForm()
            request.session['filename'] = fileName
            # Create new song object and save in database
            if Song.objects.filter(filename=fileName).count() <= 0:
                newsong = Song.objects.create_song(fileName,melodyString)
                newsong.songMelody = melodyNotes
                newsong.save()
            return render(request, 'index.html', {'file_name':fileName, 'string':str(melodyString),'form':form})
        else:
            deleteOne = randint(1, 5)
            if deleteOne == 1:
                all_songs = Song.objects.all().order_by('averageVote')
                os.remove("core/static/tuneFiles/%s.wav"%all_songs[0].filename)
                all_songs[0].delete()
            randsong = randint(1, songsNum)
            form = ScoreForm()
            while not os.path.exists("core/static/tuneFiles/tune%d.wav"%randsong):
                randsong = randint(1, songsNum)
            request.session['filename'] = 'tune'+str(randsong)
            return render(request, 'index.html', {'file_name':'tune'+str(randsong),'string':'Previously generated song: #%s'%str(randsong),'form':form})
    else:
        form = ScoreForm(request.POST)
        if form.is_valid():
            if not request.session['filename']:
                return redirect('/')
            filename_str = request.session['filename']
            # Find the Song object attached to this filename
            song = Song.objects.get(filename=filename_str)
            # Create vote
            rating = form.cleaned_data['chosenScore']
            newvote = Vote(score=rating, song=song)
            newvote.save()
            numVotesOnThisSong = int(Vote.objects.filter(song=song).count())
            song.averageVote = (song.averageVote*(numVotesOnThisSong-1) + int(newvote.score))/(numVotesOnThisSong)

            song.save()
            return redirect('/')

def combined(request):
    def combinetop4():
        all_songs = Song.objects.all().order_by('averageVote')
        chosen = [all_songs[len(all_songs)-1], all_songs[len(all_songs)-2], all_songs[len(all_songs)-3],
        all_songs[len(all_songs)-4]]
        hello = [AudioSegment.from_wav("core/static/tuneFiles/" + chosen[0].filename + ".wav"),
        AudioSegment.from_wav("core/static/tuneFiles/" + chosen[1].filename + ".wav"),
        AudioSegment.from_wav("core/static/tuneFiles/" + chosen[2].filename + ".wav"),
        AudioSegment.from_wav("core/static/tuneFiles/" + chosen[3].filename + ".wav")]
        pick = random.choice(hello)
        ultimateCombo = random.choice(hello)
        hello.remove(pick)
        for values in hello:
            pick = random.choice(hello)
            ultimateCombo = ultimateCombo + pick
            hello.remove(pick)
        filename = ("TheGlorious%r" % (random.randint(0,10000)) )
        ultimateCombo.export("core/static/combinedFiles/%s.wav" % filename, format="wav")
        request.session['filename'] = filename
        return render(request, 'combined.html', {'message': 'a song was generated', 'file_name': filename})
    def combineSquareRatio(numTunes):
        all_songs = Song.objects.all().order_by('averageVote')
        probs = []
        for song in all_songs:
            probs.append((song.averageVote+1)**2)
        totNum = np.sum(probs)
        for i in range(0,len(probs)):
            probs[i] = float(probs[i])/float(totNum)
        chosen = np.random.choice(all_songs,numTunes,replace=True,p=probs)
        combSong = AudioSegment.from_wav("core/static/tuneFiles/" + chosen[0].filename + ".wav")
        for i in range(1, len(chosen)):
            combSong += AudioSegment.from_wav("core/static/tuneFiles/" + chosen[i].filename + ".wav")
        filename = ("kewlsong%r" % (random.randint(0, 10000)))
        combSong.export("core/static/combinedFiles/%s.wav" % filename, format="wav")
        request.session['filename'] = filename
        messsage = "this nice song is generated by taking a weighted random selection of the highest ranked tunes"
        return render(request, 'combined.html', {'message': message, 'file_name': filename})
    #if Song.objects.all().count() >= 4:
    #    return combinetop4()
    numTunes = 10
    if Song.objects.all().count() >= 1:
        return combineSquareRatio(numTunes)
    else:
        return render(request, 'combined.html', {'message': 'hello!'})
def server_error(request):

    return redirect('/')

def handler404(request):

    return redirect('/')