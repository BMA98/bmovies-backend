from django.urls import path, include
from rest_framework import routers
from .viewsets import MovieViewSet, GenreViewSet, PlaylistViewSet, CollectionViewSet

router = routers.SimpleRouter()

router.register('movies', MovieViewSet)
router.register('genres', GenreViewSet)
router.register('playlists', PlaylistViewSet)
router.register('collections', CollectionViewSet)

urlpatterns = router.urls
