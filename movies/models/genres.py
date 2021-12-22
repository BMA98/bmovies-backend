from django.db import models


class Genre(models.Model):
    """
    Defines a model for Movie Genres
    genre_id: unique id
    genre: name for text
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
