from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitlesViewset, GenresViewSet, CategoriesViewSet

router_v1 = DefaultRouter()
router_v1.register(
    r'titles',
    TitlesViewset,
    basename='titles')
router_v1.register(
    r'categories',
    CategoriesViewSet,
    basename='categories')
router_v1.register(
    r'genres',
    GenresViewSet,
    basename='genres')

urlpatterns = [
    path('v1/auth/email/', SendEmail.as_view(), name='send_email'),
    path('v1/auth/token/', GetToken.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
]
