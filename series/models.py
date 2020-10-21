from django.db import models


class Series(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    original_title = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    overview = models.TextField(max_length=8096, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster = models.CharField(max_length=256, null=True, blank=True)
    backdrop = models.CharField(max_length=256, null=True, blank=True)
    language = models.ForeignKey(to='movies.Language', on_delete=models.CASCADE)
    countries = models.ManyToManyField(to='movies.ProductionCountry', blank=True)
    cast = models.ManyToManyField(to='people.Star', through='series.SeriesRole', related_name='cast_set', blank=True)
    created_by = models.ManyToManyField(to='people.People', related_name='creator_set', blank=True)
    status = models.CharField(max_length=16)
    genres = models.ManyToManyField(to='movies.Genre', blank=True)
    networks = models.ManyToManyField(to='series.Network', blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return self.original_title


class Season(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    season_number = models.IntegerField()
    original_title = models.CharField(max_length=256)
    overview = models.TextField(max_length=8096, null=True, blank=True)
    poster = models.CharField(max_length=256, null=True, blank=True)
    serie = models.ForeignKey(to='series.Series', on_delete=models.CASCADE, related_name='seasons')


class Episode(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    episode_number = models.IntegerField()
    original_title = models.CharField(max_length=256)
    overview = models.TextField(max_length=8096, null=True, blank=True)
    backdrop = models.CharField(max_length=256, null=True, blank=True)
    air_date = models.DateField(null=True, blank=True)
    season = models.ForeignKey(to='series.Season', on_delete=models.CASCADE, related_name='episodes')
    director = models.ManyToManyField(to='people.Director', blank=True)
    writer = models.ManyToManyField(to='people.ScreenWriter', blank=True)


class SeriesRole(models.Model):

    serie = models.ForeignKey(to='series.Series', on_delete=models.CASCADE)
    star = models.ForeignKey(to='people.Star', on_delete=models.CASCADE)
    role = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.role


class Network(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    logo = models.CharField(max_length=256, null=True, blank=True)
    country = models.ForeignKey(to='movies.ProductionCountry', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
