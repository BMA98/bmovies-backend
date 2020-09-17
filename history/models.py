from django.db import models
from django.utils import timezone

from users.models import MovieSeen


class MovieHistory(models.Model):
    """
    Keep track a movie history, with a specific timestamp
    user: user id, foreign key
    movie: movie id, foreign key
    channel: platform where the movie was seen
    timestamp: date and hour when the movie was seen
    """
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    channel = models.ForeignKey(to='history.Platform', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.movie)

    def save(self, *args, **kwargs):
        MovieSeen.objects.update_or_create(movie=self.movie, user=self.user)
        super(MovieHistory, self).save(*args, **kwargs)


class Platform(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name