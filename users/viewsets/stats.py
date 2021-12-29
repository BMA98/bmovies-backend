import datetime
import random

from django.http import HttpResponse
from rest_framework import viewsets

from users.models import MovieHistory, URLToken
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Sum
from django.db.models import Q


from users.serializers import MovieHistorySerializer


class DataView(viewsets.ViewSet):
    queryset = MovieHistory.objects.all()

    @action(detail=False)
    def report(self, request, **kwargs):
        if not self.authenticate(**kwargs):
            return HttpResponse(status=401)
        try:
            year = self.request.query_params['year']
            user = self.request.query_params['user_id']
        except KeyError:
            year = datetime.date.today().year
            user = self.request.user.id
        self.queryset = self.queryset.filter(user_id=user)
        self.queryset = self.queryset.filter(timestamp__year=year)
        # Count by language
        languages = self.queryset.values('movie__language') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        languages = {record['movie__language']: record['count'] for record in list(languages)}
        # Count by star
        top_stars = self.queryset.values('movie__movierole__star_id',
                                         'movie__movierole__star__name',
                                         'movie__movierole__star__profile_path') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        top_stars = [{'tmdb_id': record['movie__movierole__star_id'],
                      'name': record['movie__movierole__star__name'],
                      'count': record['count'],
                      'profile': record['movie__movierole__star__profile_path']
                      }
                     for record in list(top_stars)[:3]]
        # Add movies to count
        for star in top_stars:
            movies = self.queryset.filter(movie__cast__tmdb_id=star['tmdb_id']) \
                .values('movie__tmdb_id', 'movie__original_title', 'movie__poster',
                        'movie__backdrop', 'movie__movierole__role') \
                .distinct()
            movies = [{
                'tmdb_id': record['movie__tmdb_id'],
                'original_title': record['movie__original_title'],
                'poster': record['movie__poster'],
                'backdrop': record['movie__backdrop'],
                'role': record['movie__movierole__role']
            }
                for record in list(movies)]
            star['movies'] = movies
        # Count by directors
        top_directors = self.queryset\
            .values('movie__directors__tmdb_id', 'movie__directors__name',
                                             'movie__directors__profile_path') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        top_directors = [{'tmdb_id': record['movie__directors__tmdb_id'],
                          'name': record['movie__directors__name'],
                          'count': record['count'],
                          'profile': record['movie__directors__profile_path']}
                         for record in list(top_directors)]
        # Add movies to count
        for director in top_directors:
            movies = self.queryset\
                .filter(movie__directors__tmdb_id=director['tmdb_id']) \
                .values('movie__tmdb_id', 'movie__original_title', 'movie__poster', 'movie__backdrop') \
                .distinct()
            movies = [{
                'tmdb_id': record['movie__tmdb_id'],
                'original_title': record['movie__original_title'],
                'poster': record['movie__poster'],
                'backdrop': record['movie__backdrop']
            }
                for record in list(movies)]
            director['movies'] = movies
        # Count by screenwriters
        top_screenwriters = self.queryset.values('movie__screenwriters__tmdb_id', 'movie__screenwriters__name') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('-count')
        top_screenwriters = [{'tmdb_id': record['movie__screenwriters__tmdb_id'],
                              'name': record['movie__screenwriters__name'],
                              'count': record['count']}
                             for record in list(top_screenwriters)]
        # Count by photography director
        top_photography_directors = self.queryset\
            .values('movie__photography_directors__tmdb_id',
                    'movie__photography_directors__name') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('-count')
        top_photography_directors = [{'tmdb_id': record['movie__photography_directors__tmdb_id'],
                                      'name': record['movie__photography_directors__name'],
                                      'count': record['count']}
                                     for record in list(top_photography_directors)]
        # Count by month
        monthly_viewing = self.queryset.values('timestamp__month') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('timestamp__month')
        tmp = [0] * 12
        for record in list(monthly_viewing):
            tmp[record['timestamp__month'] - 1] = record['count']
        monthly_viewing = tmp
        # Sum runtime
        total_runtime = self.queryset.aggregate(Sum('movie__runtime'))
        # Count by genre
        genres = self.queryset.values('movie__genres__id', 'movie__genres__name') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        genres = {record['movie__genres__name']: {'id': record['movie__genres__id'], 'count': record['count']} for record in list(genres)}
        # Count by country
        countries = self.queryset.values('movie__countries__iso') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        countries = {record['movie__countries__iso']: record['count'] for record in list(countries)}
        # Total movies
        total = MovieHistory.objects.filter(timestamp__year=year).distinct('movie_id').count()
        history = self.queryset.order_by('timestamp') \
            .values('id',
                    'movie__tmdb_id',
                    'movie__original_title',
                    'timestamp',
                    'movie__poster',
                    'movie__backdrop')
        history = [{'id': record['id'],
                    'tmdb_id': record['movie__tmdb_id'],
                    'original_title': record['movie__original_title'],
                    'timestamp': record['timestamp'],
                    'poster': record['movie__poster'],
                    'backdrop': record['movie__backdrop'],
                    } for record in history]
        response = {'top_languages': languages,
                    'top_stars': top_stars[:3],
                    'top_directors': top_directors[:3],
                    'top_screenwriters': top_screenwriters[:3],
                    'top_photography_directors': top_photography_directors[:3],
                    'minutes': total_runtime['movie__runtime__sum'],
                    'monthly_viewing': monthly_viewing,
                    'top_genres': genres,
                    'countries': countries,
                    'total': total,
                    'history': history,
                    }
        return Response(response)

    def authenticate(self, **kwargs):
        if self.request.user.is_authenticated:
            return True
        else:
            token = self.request.query_params['token']
            x = URLToken.objects.filter(user=self.request.query_params['user_id'], token=token).count()
            return x >= 1

    @action(detail=False)
    def top_stars(self, request, **kwargs):
        if not self.authenticate(**kwargs):
            return HttpResponse(status=401)
        try:
            user = self.request.query_params['user_id']
            year = self.request.query_params['year']
        except KeyError:
            user = self.request.user.id
            year = datetime.date.today().year
        self.queryset = self.queryset.filter(user_id=user)
        top_stars = self.queryset \
            .values('movie__movierole__star_id',
                    'movie__movierole__star__name',
                    'movie__movierole__star__profile_path') \
            .annotate(count=Count('movie__tmdb_id', distinct=True)) \
            .order_by('-count')
        top_stars = [{'tmdb_id': record['movie__movierole__star_id'],
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
        # top_star = tmp[random.randint(0, len(tmp) - 1)]
        movies = self.queryset.filter(timestamp__year=year, movie__movierole__star_id__in=top_star_ids) \
            .values('movie__movierole__star_id',
                    'movie__movierole__star__profile_path',
                    'movie__movierole__star__name',
                    'movie__movierole__movie__original_title',
                    'movie__movierole__movie__tmdb_id',
                    'movie__movierole__movie__poster',
                    )
        movies_dict = {}
        for movie in movies:
            if movie['movie__movierole__star_id'] in movies_dict:
                movies_dict[movie['movie__movierole__star_id']]['movies'] \
                    .append(
                    {
                        'tmdb_id': movie['movie__movierole__movie__tmdb_id'],
                        'original_title': movie['movie__movierole__movie__original_title'],
                        'poster': movie['movie__movierole__movie__poster'],
                    })

            else:
                movies_dict[movie['movie__movierole__star_id']] = {
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
        if not self.authenticate(**kwargs):
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
        movies = self.queryset\
            .values('movie__tmdb_id', 'movie__original_title', 'movie__poster', 'movie__backdrop')\
            .distinct()
        movies = [{
            'tmdb_id': movie['movie__tmdb_id'],
            'original_title': movie['movie__original_title'],
            'poster': movie['movie__poster'],
            'backdrop': movie['movie__backdrop'],
        } for movie in movies]
        return Response(list(movies))