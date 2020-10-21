from rest_framework import routers
from .viewsets import SeriesViewsSet, SeasonViewSet

router = routers.SimpleRouter()

router.register('series', SeriesViewsSet)
router.register('season', SeasonViewSet)

urlpatterns = router.urls
