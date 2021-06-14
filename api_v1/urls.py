from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitlesViewSet, GenresViewSet, CategoriesViewSet


router = DefaultRouter()
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router.urls)),
]
