import datetime
import random

from django.http import HttpResponse
from rest_framework import viewsets

from users.models import MovieHistory, URLToken
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Sum


class DataView(viewsets.ViewSet):
    queryset = MovieHistory.objects.prefetch_related('movie', 'user').all()

    @action(detail=False)
    def report(self, request, **kwargs):
        """
        Endpoint for Year in Review
        """
        if not self._authenticate(**kwargs):
            return HttpResponse(status=401)
        try:
            year = self.request.query_params['year']
            user = self.request.query_params['user_id']
        except KeyError:
            year = datetime.date.today().year
            user = self.request.user.id
        self.queryset = self.queryset.filter(user_id=user)
        self.queryset = self.queryset.filter(timestamp__year=year)
        response = {'top_languages': self._get_languages(),
                    'top_stars': self._get_top_stars(),
                    'top_directors': self._get_top_people('directors'),
                    'top_screenwriters:': self._get_top_people('screenwriters'),
                    'top_photography_directors': self._get_top_people('photography_directors'),
                    'minutes': self.queryset.aggregate(Sum('movie__runtime'))['movie__runtime__sum'],
                    'monthly_viewing': self._get_monthly_viewing(),
                    'top_genres': self._get_genres(),
                    'countries': self._get_countries(),
                    'total': MovieHistory.objects.filter(timestamp__year=year).order_by().distinct('movie').count(),
                    'history': self._get_history(),
                    'platforms': self._get_top_platforms(),
                    }
        return Response(response)

    def _authenticate(self, **kwargs):
        """
        Authentication by key or URL Token
        """
        if self.request.user.is_authenticated:
            return True
        else:
            token = self.request.query_params['token']
            x = URLToken.objects.filter(user=self.request.query_params['user_id'], token=token).count()
            return x >= 1

    @action(detail=False)
    def top_stars(self, request, **kwargs):
        """
        Endpoint for getting the top stars across time and
        the subset of movies seen this year that includes them
        """
        if not self._authenticate(**kwargs):
            return HttpResponse(status=401)
        try:
            user = self.request.query_params['user_id']
            year = self.request.query_params['year']
        except KeyError:
            user = self.request.user.id
            year = datetime.date.today().year
        self.queryset = self.queryset.filter(user_id=user)
        top_stars = self.queryset \
            .values('movie__movierole__star__tmdb_id',
                    'movie__movierole__star__name',
                    'movie__movierole__star__profile_path') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        top_stars = [{'tmdb_id': record['movie__movierole__star__tmdb_id'],
                      'name': record['movie__movierole__star__name'],
                      'count': record['count'],
                      'profile': record['movie__movierole__star__profile_path']
                      }
                     for record in list(top_stars)]
        max = top_stars[0]['count']
        top_star_ids = []
        for star in top_stars:
            if star['count'] == max:
                top_star_ids.append(star['tmdb_id'])
            else:
                break
        movies = self.queryset.filter(timestamp__year=year, movie__movierole__star_id__in=top_star_ids) \
            .values('movie__movierole__star__tmdb_id',
                    'movie__movierole__star__profile_path',
                    'movie__movierole__star__name',
                    'movie__movierole__movie__original_title',
                    'movie__movierole__movie__tmdb_id',
                    'movie__movierole__movie__poster',
                    )
        movies_dict = {}
        for movie in movies:
            if movie['movie__movierole__star__tmdb_id'] in movies_dict:
                movies_dict[movie['movie__movierole__star__tmdb_id']]['movies'] \
                    .append(
                    {
                        'tmdb_id': movie['movie__movierole__movie__tmdb_id'],
                        'original_title': movie['movie__movierole__movie__original_title'],
                        'poster': movie['movie__movierole__movie__poster'],
                    })

            else:
                movies_dict[movie['movie__movierole__star__tmdb_id']] = {
                    'name': movie['movie__movierole__star__name'],
                    'count': max,
                    'profile_path': movie['movie__movierole__star__profile_path'],
                    'movies': [{
                        'tmdb_id': movie['movie__movierole__movie__tmdb_id'],
                        'original_title': movie['movie__movierole__movie__original_title'],
                        'poster': movie['movie__movierole__movie__poster'],
                    }]
                }
        return Response(movies_dict)

    @action(detail=False)
    def movies(self, request, **kwargs):
        """
        Filters the history queryset by params in the requests.
        They can be language, country, month or genre
        """
        if not self._authenticate(**kwargs):
            return HttpResponse(status=401)
        try:
            user = self.request.query_params['user_id']
            year = self.request.query_params['year']
        except KeyError:
            user = self.request.user.id
            year = datetime.date.today().year
        self.queryset = self.queryset.filter(user_id=user, timestamp__year=year)
        if 'language' in self.request.query_params:
            self.queryset = self.queryset.filter(movie__language=self.request.query_params['language'])
        if 'country' in self.request.query_params:
            self.queryset = self.queryset.filter(movie__countries__iso=self.request.query_params['country'])
        if 'month' in self.request.query_params:
            self.queryset = self.queryset.filter(timestamp__month=self.request.query_params['month'])
        if 'genre' in self.request.query_params:
            self.queryset = self.queryset.filter(movie__genres__id=self.request.query_params['genre'])
        if 'platform' in self.request.query_params:
            self.queryset = self.queryset.filter(channel__name=self.request.query_params['platform'])
        movies = self.queryset \
            .values('movie__tmdb_id', 'movie__original_title', 'movie__overview', 'movie__poster', 'movie__backdrop', 'timestamp') \
            .distinct()
        movies = [{
            'tmdb_id': movie['movie__tmdb_id'],
            'original_title': movie['movie__original_title'],
            'overview': movie['movie__overview'],
            'poster': movie['movie__poster'],
            'backdrop': movie['movie__backdrop'],
            'timestamp': movie['timestamp']
        } for movie in movies]
        return Response(list(movies))

    def _get_languages(self):
        """
        Returns a dictionary with language ISO codes as keys and the number of movies in each language
        """
        languages = self.queryset.values('movie__language') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        languages = {record['movie__language']: record['count'] for record in list(languages)}
        return languages

    def _get_top_stars(self):
        """
        Returns a list with the top three stars
        """
        top_stars = self.queryset.values('movie__movierole__star__tmdb_id',
                                         'movie__movierole__star__name',
                                         'movie__movierole__star__profile_path') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        top_stars = [{'tmdb_id': record['movie__movierole__star__tmdb_id'],
                      'name': record['movie__movierole__star__name'],
                      'count': record['count'],
                      'profile': record['movie__movierole__star__profile_path']
                      }
                     for record in list(top_stars)[:3]]
        for star in top_stars:
            movies = self.queryset\
                .filter(movie__movierole__star__tmdb_id=star['tmdb_id']) \
                .values('movie__tmdb_id', 'movie__original_title', 'movie__overview', 'movie__poster', 'movie__backdrop') \
                .distinct()
            movies = [{
                'tmdb_id': record['movie__tmdb_id'],
                'original_title': record['movie__original_title'],
                'overview': record['movie__overview'],
                'poster': record['movie__poster'],
                'backdrop': record['movie__backdrop']
            }
                for record in list(movies)]
            star['movies'] = movies
        return top_stars

    def _get_top_people(self, role):
        """
        Returns a list with top three people (directors, screenwriters, photography directors)
        """
        top_people = self.queryset \
            .values(f'movie__{role}__tmdb_id', f'movie__{role}__name',
                    f'movie__{role}__profile_path') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        top_people = [{'tmdb_id': record[f'movie__{role}__tmdb_id'],
                       'name': record[f'movie__{role}__name'],
                       'count': record['count'],
                       'profile': record[f'movie__{role}__profile_path']}
                      for record in list(top_people)[:3]]
        # Add movies to count
        for people in top_people:
            lookup = {
                f'movie__{role}__tmdb_id': people['tmdb_id']
            }
            movies = self.queryset \
                .filter(**lookup) \
                .values('movie__tmdb_id', 'movie__original_title', 'movie__overview', 'movie__poster', 'movie__backdrop') \
                .distinct()
            movies = [{
                'tmdb_id': record['movie__tmdb_id'],
                'overview': record['movie__overview'],
                'original_title': record['movie__original_title'],
                'poster': record['movie__poster'],
                'backdrop': record['movie__backdrop']
            }
                for record in list(movies)]
            people['movies'] = movies
        return top_people

    def _get_monthly_viewing(self):
        """
        A list where each element is the number of movies seen by month
        """
        monthly_viewing = self.queryset.values('timestamp__month') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('timestamp__month')
        tmp = [0] * 12
        for record in list(monthly_viewing):
            tmp[record['timestamp__month'] - 1] = record['count']
        return tmp

    def _get_genres(self):
        """
        A dictionary with the count of movies seen by genre
        """
        genres = self.queryset.values('movie__genres__id', 'movie__genres__name') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        genres = {record['movie__genres__name']: {'id': record['movie__genres__id'], 'count': record['count']} for
                  record in list(genres)}
        return genres

    def _get_countries(self):
        """
        A dictionary with the count of movies seen by country
        """
        countries = self.queryset.values('movie__countries__iso') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        countries = {record['movie__countries__iso']: record['count'] for record in list(countries)}
        return countries

    def _get_history(self):
        """
        Returns a list with the dictionary sorted from old to new
        """
        history = self.queryset.order_by('timestamp') \
            .values('id',
                    'movie__tmdb_id',
                    'movie__original_title',
                    'movie__overview',
                    'timestamp',
                    'movie__poster',
                    'movie__backdrop')
        history = [{'id': record['id'],
                    'tmdb_id': record['movie__tmdb_id'],
                    'original_title': record['movie__original_title'],
                    'overview': record['movie__overview'],
                    'timestamp': record['timestamp'],
                    'poster': record['movie__poster'],
                    'backdrop': record['movie__backdrop'],
                    } for record in history]
        return history

    def _get_top_platforms(self):
        """

        """
        platforms = self.queryset.values('channel__name') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        platforms = {record['channel__name']: record['count'] for record in list(platforms)}
        return platforms
