from django.db import models

from users.models.mixins import UserMovieOnHistoryMixin, UserMovieUpdatableMixin


class MovieReview(UserMovieOnHistoryMixin, UserMovieUpdatableMixin):
    """
    Keeps track of movie reviews by each user
    """
    comment = models.TextField(max_length=10000)

    class Meta:
        unique_together = (('user', 'movie'),)
