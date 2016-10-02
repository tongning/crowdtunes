from django.db import models

# Create your models here.


class SongManager(models.Manager):
    def create_song(self, filename, note_sequence):
        song = self.create(filename=filename,note_sequence=note_sequence)
        return song
class Song(models.Model):

    filename = models.CharField(max_length=200)

    note_sequence = models.CharField(max_length=200)
    objects = SongManager()
    averageVote = models.FloatField(default=0)


class Vote(models.Model):
    score = models.IntegerField(default=0)
    song = models.ForeignKey(Song)
