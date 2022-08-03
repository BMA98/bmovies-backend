from django.utils import timezone

from users.models.mixins.abstract_models import UserMovie, CreatedUpdated


class UserMovieUpdatableMixin(UserMovie, CreatedUpdated):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(UserMovieUpdatableMixin, self).save(*args, **kwargs)