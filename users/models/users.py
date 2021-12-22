from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from users.managers import UserManager
from users.models import MovieHistory


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
    favorites_movies = models.ManyToManyField(to='movies.Movie', related_name='favorite_movies', blank=True, through='users.UserFavoriteMovie')
    movie_history = models.ManyToManyField(to='movies.Movie', related_name='movies_seen', blank=True, through=MovieHistory)
    #url_tokens = models.ForeignKey(to='users.URLToken', related_query_name='url_tokens', on_delete=models.CASCADE, null=True, blank=True)

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