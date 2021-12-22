from django.db import models


class MovieRole(models.Model):
    """
    Defines a role, given a movie and a movie star
    movie: the movie id, foreign key
    star: the star id, foreign key
    role: the character name, optional
    """
    movie = models.ForeignKey(to='movies.Movie', on_delete=models.CASCADE)
    star = models.ForeignKey(to='people.Star', on_delete=models.CASCADE)
    role = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.role
