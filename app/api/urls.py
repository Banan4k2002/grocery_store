from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryList, ProductViewSet

router = DefaultRouter()

router.register(r'products', ProductViewSet)

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
