from django.urls import path, include
from rest_framework import routers
from .viewsets import StarViewSet, PeopleViewSet

router = routers.SimpleRouter()

router.register('stars', StarViewSet)
router.register('people', PeopleViewSet)

urlpatterns = router.urls