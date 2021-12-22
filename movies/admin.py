from django.contrib import admin
from .models import Movie, Genre, MovieRole, Track, MovieTrack

# Register your models here.

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieRole)
admin.register(Track)
admin.register(MovieTrack)
