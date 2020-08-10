from django.db import models
from iso_language_codes import language


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
    """
    tmdb_id = models.IntegerField(primary_key=True)
    imdb_id = models.IntegerField(null=True, blank=True)
    original_title = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True)
    overview = models.CharField(max_length=8192, null=True, blank=True)
    poster = models.CharField(max_length=256, null=True, blank=True)
    backdrop = models.CharField(max_length=256, null=True, blank=True)
    language = models.ForeignKey(to='Language', on_delete=models.CASCADE)
    trailer = models.CharField(max_length=1024, blank=True, null=True)
    director = models.ManyToManyField(to='people.Director', blank=True)
    photography_director = models.ManyToManyField(to='people.PhotographyDirector', blank=True)
    screenwriter = models.ManyToManyField(to='people.ScreenWriter', blank=True)
    producer = models.ManyToManyField(to='people.Producer', blank=True)
    cast = models.ManyToManyField(to='people.Star', blank=True)
    genres = models.ManyToManyField(to='Genre', blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return self.original_title


class Genre(models.Model):
    """
    Defines a model for Movie Genres
    genre_id: unique id
    genre: name for text
    """
    genre_id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=256)

    def __str__(self):
        return self.genre


class Language(models.Model):
    """
    Defines a model for Languages
    language_id: unique id
    language_iso: unique ISO identifier
    """
    language_id = models.IntegerField(primary_key=True)
    language_iso = models.CharField(max_length=32)

    def __str__(self):
        return language(self.language_iso)['Name']
