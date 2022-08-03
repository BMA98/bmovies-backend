from django.core.exceptions import PermissionDenied

from users.models.mixins.abstract_models import UserMovie, CreatedUpdated


class UserMovieOnHistoryMixin(UserMovie, CreatedUpdated):
    class Meta:

        abstract = True

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        :return:
        """
        from users.models import MovieHistory
        seen = MovieHistory.objects.filter(movie=self.movie, user=self.user).exists()
        if seen:
            return super(UserMovieOnHistoryMixin, self).save(*args, **kwargs)
        else:
            raise PermissionDenied(f'{self.movie} has not been seen by user {self.user}')
