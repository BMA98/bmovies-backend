from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from movies.models import Movie
from people.models import People
from users.managers import UserManager


class MovieSeen(models.Model):
    """
    MovieSeen keeps track of the movies seen by the user
    """
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'movie'),)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class which includes favorites movies, favorites people
    """
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True
    )
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    favorites_movies = models.ManyToManyField(to=Movie, related_name='favorite_movies', blank=True)
    favorites_stars = models.ManyToManyField(to='people.Star', related_name='favorite_stars',blank=True)
    favorites_directors = models.ManyToManyField(to='people.Star', related_name='favorite_directors', blank=True)
    movies_seen = models.ManyToManyField(to=Movie, related_name='movies_seen', blank=True, through=MovieSeen)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name + ' ' + self.lastname

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?"
        :param app_label:
        :return:
        """
        # Simplest possible answer: Yes, always
        return True
