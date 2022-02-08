from django.db import models


class PlaylistRecord(models.Model):
    '''
    A model for records in a playlist.
    pos: integer for sorting purposes, should not be confused with the primary key
    movie: the key of the movie which is being added
    description: a small comment, optional
    '''
    order = models.IntegerField(blank=True, null=True, auto_created=True)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    playlist = models.ForeignKey(to='movies.Playlist', on_delete=models.CASCADE)
    description = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return str(self.playlist) + ' - ' + str(self.movie)

    class Meta:
        ordering = ('playlist', 'order', )


class Playlist(models.Model):
    '''
    A Playlist is a set of movies ordered thematically
    '''
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True, null=True)
    movies = models.ManyToManyField(to='movies.Movie', through=PlaylistRecord)

    def __str__(self):
        return self.name


class CollectionRecord(models.Model):
    order = models.IntegerField(blank=True, null=True, auto_created=True)
    playlist = models.ForeignKey(to='movies.Playlist', on_delete=models.CASCADE)
    collection = models.ForeignKey(to='movies.Collection', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.collection) + ' - ' + str(self.playlist)

    class Meta:
        ordering = ('collection', 'order')


class Collection(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True, null=True)
    playlists = models.ManyToManyField(to=Playlist, through=CollectionRecord)

    def __str__(self):
        return self.name
