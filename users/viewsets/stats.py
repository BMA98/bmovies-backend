import datetime

from django.http import HttpResponse
from rest_framework import viewsets

from users.models import MovieHistory, URLToken
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Sum


class DataView(viewsets.ViewSet):
    queryset = MovieHistory.objects.all()

    @action(detail=False)
    def report(self, request, **kwargs):
        print(f'Authentication: {self.authenticate(**kwargs)}')
        if not self.authenticate(**kwargs):
            return HttpResponse(status=401)
        try:
            year = self.request.query_params["year"]
        except KeyError:
            year = datetime.date.today().year
        if request.user.id:
            self.queryset = self.queryset.filter(user_id=request.user.id)
        self.queryset = self.queryset.filter(timestamp__year=year)
        # Count by language
        languages = self.queryset.values('movie__language') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('-count')
        languages = {record['movie__language']: record['count'] for record in list(languages)}
        # Count by star
        top_stars = self.queryset.values('movie__movierole__star_id',
                                         'movie__movierole__star__name',
                                         'movie__movierole__star__profile_path') \
            .annotate(count=Count('movie__tmdb_id')) \
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
        top_directors = self.queryset.values('movie__directors__tmdb_id', 'movie__directors__name',
                                             'movie__directors__profile_path') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('-count')
        top_directors = [{'tmdb_id': record['movie__directors__tmdb_id'],
                          'name': record['movie__directors__name'],
                          'count': record['count'],
                          'profile': record['movie__directors__profile_path']}
                         for record in list(top_directors)]
        # Add movies to count
        for director in top_directors:
            movies = self.queryset.filter(movie__directors__tmdb_id=director['tmdb_id']) \
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
        top_photography_directors = self.queryset.values('movie__photography_directors__tmdb_id',
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
        monthly_viewing = [record['count'] for record in list(monthly_viewing)]
        # Sum runtime
        total_runtime = self.queryset.aggregate(Sum('movie__runtime'))
        # Count by genre
        genres = self.queryset.values('movie__genres__name') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('-count')
        genres = {record['movie__genres__name']: record['count'] for record in list(genres)}
        # Count by country
        countries = self.queryset.values('movie__countries__iso') \
            .annotate(count=Count('movie__tmdb_id')) \
            .order_by('-count')
        countries = {record['movie__countries__iso']: record['count'] for record in list(countries)}
        # Total movies
        total = MovieHistory.objects.filter(timestamp__year=year).distinct('movie_id').count()
        response = {'top_languages': languages,
                    'top_stars': top_stars[:3],
                    'top_directors': top_directors[:3],
                    'top_screenwriters': top_screenwriters[:3],
                    'top_photography_directors': top_photography_directors[:3],
                    'minutes': total_runtime['movie__runtime__sum'],
                    'monthly_viewing': monthly_viewing,
                    'top_genres': genres,
                    'countries': countries,
                    'total': total
                    }
        # Count by country
        return Response(response)

    def authenticate(self, **kwargs):
        if self.request.user.is_authenticated:
            return True
        else:
            token = self.request.query_params['token']
            print(self.request.query_params['user_id'])
            print(self.request.query_params['token'])
            x = URLToken.objects.filter(user=self.request.query_params['user_id'], token=token).count()
            #print(x)
            return x >= 1
