from django.urls import path, include
from rest_framework import routers
from .viewsets import MovieViewSet, GenreViewSet, LanguageViewSet

router = routers.SimpleRouter()

router.register('movies', MovieViewSet)
router.register('genres', GenreViewSet)
router.register('languages', LanguageViewSet)

urlpatterns = router.urls
