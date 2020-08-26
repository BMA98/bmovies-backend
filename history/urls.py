from rest_framework import routers

from .viewsets import MovieHistoryViewSet

router = routers.SimpleRouter()

router.register('history', MovieHistoryViewSet)

urlpatterns = router.urls
