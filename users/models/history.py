from django.db import models
from django.utils import timezone
from users.models.mixins import UserMovieUpdatableMixin


class MovieHistory(UserMovieUpdatableMixin):
    """
    MovieHistory keeps track of the movies seen by the user
    channel: primary key to the channel where movie has been seen (cinema, netflix, plex, etc)
    timestamp: the viewing timestamp, can be null
    """
    channel = models.ForeignKey(to='users.Channel', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        """
        We force that a specific user can see only one specific movie at a one specific time.
        Repeated viewings should be keep as independent records
        """
        unique_together = (('user', 'movie', 'timestamp'),)
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user} - {self.movie}'
