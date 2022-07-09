from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.viewsets import MovieHistoryViewSet, MovieRankViewSet, UserFavoriteMovieViewSet, \
    UsersViewSet, DataView

router = SimpleRouter()
router.register('users/ranks', MovieRankViewSet)
router.register('users/history', MovieHistoryViewSet)
router.register('users/favorites', UserFavoriteMovieViewSet)
router.register('users', UsersViewSet)
#router.register('ranks', MovieOnlyRankViewSet)
router.register('stats', DataView)
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    url(r'user/auth/', include('rest_auth.urls')),
    url(r'user/registration/', include('rest_auth.registration.urls')),
]