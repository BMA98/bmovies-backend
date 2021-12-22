from django.urls import path, include
from rest_framework import routers
from .viewsets import MovieViewSet, GenreViewSet

router = routers.SimpleRouter()

router.register('movies', MovieViewSet)
router.register('genres', GenreViewSet)

urlpatterns = router.urls
