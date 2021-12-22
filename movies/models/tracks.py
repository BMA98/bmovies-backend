from django.db import models


class Track(models.Model):
    """
    Defines a mode for tracks
    name: the name of the track.
    artist: the name of the artist.
    spotify: path to spotify track.
    """
    name = models.CharField(max_length=256)
    artist = models.CharField(max_length=256)
    spotify = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.name


class MovieTrack(models.Model):
    """
    Defines a many to many relation between movies and tracks
    movie: the movie id.
    track: the song id.
    """
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    track = models.ForeignKey(to='movies.Track', on_delete=models.CASCADE)