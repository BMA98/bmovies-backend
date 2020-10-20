from rest_framework import routers

from .viewsets import MovieHistoryViewSet, MovieHistoryUniqueViewSet

router = routers.SimpleRouter()

router.register('rest-auth/user/history/unique', MovieHistoryUniqueViewSet)
router.register('rest-auth/user/history', MovieHistoryViewSet)


urlpatterns = router.urls
