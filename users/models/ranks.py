from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from users.models import MovieHistory
from users.models.mixins import UserMovieUpdatableMixin, UserMovieOnHistoryMixin


class MovieRank(UserMovieUpdatableMixin, UserMovieOnHistoryMixin):
    """
    Keeps track of movie ranks by each user
    0 disliked, 1 liked, 2 loved
    """
    ranking = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(2)))

    class Meta:
        unique_together = (('user', 'movie'),)
