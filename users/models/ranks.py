from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from users.models import MovieHistory


class MovieRank(models.Model):
    """
    Keeps track of movie ranks by each user
    0 disliked, 1 liked, 2 loved
    """
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    ranking = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(2)))
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(null=True)

    class Meta:
        unique_together = (('user', 'movie'),)

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        :return:
        """
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        seen = MovieHistory.objects.filter(movie=self.movie, user=self.user).exists()
        if seen:
            return super(MovieRank, self).save(*args, **kwargs)
        else:
            raise PermissionDenied(f'{self.movie} has not been seen by user {self.user}')