from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.viewsets import MovieSeenViewSet, MovieRankViewSet, MovieOnlyRankViewSet, UserFavoriteMovieViewSet, \
    UserFullFavoriteMovieViewSet

router = SimpleRouter()
router.register('rest-auth/user/movies/ranks', MovieRankViewSet)
router.register('rest-auth/user/movies/seen', MovieSeenViewSet)
router.register('rest-auth/user/movies/favorites/full', UserFullFavoriteMovieViewSet)
router.register('rest-auth/user/movies/favorites', UserFavoriteMovieViewSet)
router.register('ranks', MovieOnlyRankViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]