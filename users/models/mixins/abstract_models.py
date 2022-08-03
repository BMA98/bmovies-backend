from django.db import models


class UserMovie(models.Model):
    """
    An abstract model providing fields user and movie
    """

    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CreatedUpdated(models.Model):
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
