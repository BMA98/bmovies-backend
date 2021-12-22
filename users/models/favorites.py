from django.db import models
from django.utils import timezone


class UserFavoriteMovie(models.Model):
    """
    Keeps track of favorite movies for each user
    """
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)

    class Meta:
        unique_together = (('user', 'movie'),)

    def save(self, *args, **kwargs):
        """
        Creates timestamps on save
        :return:
        """
        if not self.id:
            self.created = timezone.now()
        return super(UserFavoriteMovie, self).save(*args, **kwargs)
