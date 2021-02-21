from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.viewsets import MovieSeenViewSet, MovieRankViewSet, MovieOnlyRankViewSet, UserFavoriteMovieViewSet, \
    UserFullFavoriteMovieViewSet, MovieDetailedRankViewSet, UsersViewSet, UserTopStars, UserTopScreenwriters, \
    UserTopPhotographyDirectors, UserTopDirectors, UserLanguagesCount

router = SimpleRouter()
router.register('rest-auth/user/movies/ranks/detail', MovieDetailedRankViewSet)
router.register('rest-auth/user/movies/ranks', MovieRankViewSet)
router.register('rest-auth/user/movies/seen', MovieSeenViewSet)
router.register('rest-auth/user/movies/favorites/full', UserFullFavoriteMovieViewSet)
router.register('rest-auth/user/movies/favorites', UserFavoriteMovieViewSet)
router.register('rest-auth/user/stars', UserTopStars)
router.register('rest-auth/user/directors', UserTopDirectors)
router.register('rest-auth/user/photography_directors', UserTopPhotographyDirectors)
router.register('rest-auth/user/screenwriters', UserTopScreenwriters)
router.register('rest-auth/user/stats/languages', UserLanguagesCount)
router.register('rest-auth/users', UsersViewSet)
router.register('ranks', MovieOnlyRankViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]