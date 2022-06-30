from django.db import models
from django.utils import timezone


class MovieHistory(models.Model):
    """
    MovieHistory keeps track of the movies seen by the user
    user: the primary key to the user
    movie: the primary key to the movie
    channel: primary key to the channel where movie has been seen (cinema, netflix, plex, etc)
    timestamp: the viewing timestamp, can be null
    """
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    channel = models.ForeignKey(to='users.Channel', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(null=True)


    class Meta:
        """
        We force that a specific user can see only one specific movie at a one specific time.
        Repeated viewings should be keep as independent records
        """
        unique_together = (('user', 'movie', 'timestamp'),)
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user} - {self.movie}'

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        :return:
        """
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(MovieHistory, self).save(*args, **kwargs)