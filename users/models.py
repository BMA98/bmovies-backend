from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from movies.models import Movie
from people.models import People
from users.managers import UserManager


class MovieSeen(models.Model):
    """
    MovieSeen keeps track of the movies seen by the user
    """
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
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
        return super(MovieSeen, self).save(*args, **kwargs)


class MovieRank(models.Model):
    """
    Keeps track of movie ranks by each user
    """
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    ranking = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(10)))
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
        seen = MovieSeen.objects.filter(movie=self.movie, user=self.user).exists()
        if seen:
            return super(MovieRank, self).save(*args, **kwargs)
        else:
            raise PermissionDenied(f'{self.movie} has not been seen by user {self.user}')


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
    favorites_movies = models.ManyToManyField(to=Movie, related_name='favorite_movies', blank=True, through='users.UserFavoriteMovie')
    #favorites_stars = models.ManyToManyField(to='people.Star', related_name='favorite_stars',blank=True)
    #favorites_directors = models.ManyToManyField(to='people.Star', related_name='favorite_directors', blank=True)
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
