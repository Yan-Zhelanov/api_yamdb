from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SendEmail, GetToken, CommentViewSet, ReviewViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/email/', SendEmail.as_view(), name='send_email'),
    path('v1/auth/token/', GetToken.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
]
