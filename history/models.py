from django.db import models
from django.utils import timezone


class MovieHistory(models.Model):

    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.movie)