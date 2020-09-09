from rest_framework import routers

from .viewsets import MovieHistoryViewSet

router = routers.SimpleRouter()

router.register('rest-auth/user/history', MovieHistoryViewSet)

urlpatterns = router.urls
