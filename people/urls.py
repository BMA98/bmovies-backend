from django.urls import path, include
from rest_framework import routers
from .viewsets import PeopleViewSet

router = routers.SimpleRouter()

router.register('people', PeopleViewSet)

urlpatterns = router.urls