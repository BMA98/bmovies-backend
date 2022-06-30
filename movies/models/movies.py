from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Movie(models.Model):
    """
    Defines a model for Movie, the basic element of the platform
    tmdb_id: unique identifier from TMDb
    imdb_id: (optional) unique identifier from IMDb
    original_title: title in the original language
    title: title in the local language
    release_date: (optional) date of theatrical release (from TMDb)
    runtime: (optional) runtime of the movie
    overview: (optional) summary of the movie
    poster: (optional) path to the poster
    backdrop: (optional) path to the backdrop image
    trailer: path to youtube trailer
    director: all people credited as directors
    photography_director: all people credited as photography director
    screenwriter: all people credited as screenwriter
    producer: all people credited as producer
    cast: all people credited as cast
    genres: all movie genres
    status: 0 for seen, 1 for high priority, 2 for possible viewing, 3 for low priority
    """
    tmdb_id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=16, null=True, blank=True)
    original_title = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    year = models.IntegerField(validators=(MinValueValidator(1888), MaxValueValidator(2100)), null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True)
    overview = models.TextField(max_length=8096, null=True, blank=True)
    poster = models.CharField(max_length=256, null=True, blank=True)
    backdrop = models.CharField(max_length=256, null=True, blank=True)
    language = models.CharField(max_length=8)
    countries = models.ManyToManyField(to='movies.Country', blank=True)
    trailer = models.CharField(max_length=1024, blank=True, null=True)
    directors = models.ManyToManyField(to='people.People', related_name='director_roles', blank=True)
    photography_directors = models.ManyToManyField(to='people.People', related_name='photography_roles', blank=True)
    screenwriters = models.ManyToManyField(to='people.People', related_name='screenwriter_roles', blank=True)
    cast = models.ManyToManyField(to='people.People', through='movies.MovieRole', related_name='cast_roles', blank=True)
    genres = models.ManyToManyField(to='movies.Genre', blank=True)
    songs = models.ManyToManyField(to='movies.Track', through='movies.MovieTrack', blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return self.original_title
