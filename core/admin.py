from django.contrib import admin

# Register your models here.
from .models import Song, Vote
admin.site.register(Song)
admin.site.register(Vote)