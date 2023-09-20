from rest_framework.routers import DefaultRouter

from messaging.views import UserViewSet, MessageViewSet

router = DefaultRouter()
router.register('messages', MessageViewSet, basename='message')
router.register('users', UserViewSet, basename='user')
urlpatterns = router.urls
