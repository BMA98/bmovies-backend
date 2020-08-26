from django.db import models


class People(models.Model):
    """
    Defines an abstract model for People
    tmdb_id: the unique identifier from TMDb
    imdb_id: (optional) the unique identifier from IMDb
    name: name
    biography: (optional) biografy
    gender: unique identifier for gender, default 0 (unknown)
    profile_path: (optional) path to TMDb profile pic
    birthday: (optional) date of birth
    deathday: (optional) date of death, null if still alive
    """
    tmdb_id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=1024)
    biography = models.CharField(max_length=8192, null=True, blank=True)
    gender = models.IntegerField(default=0)
    profile_path = models.CharField(max_length=1024, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Star(People):
    """
    For actors and actresses
    """
    pass


class Director(People):
    """
    For movie directors
    """
    pass


class PhotographyDirector(People):
    """
    For photography directors
    """
    pass


class ScreenWriter(People):
    """
    For screenwriters.
    """
    pass


class Producer(People):
    """
    For producers
    """
    pass
