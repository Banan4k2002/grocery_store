from django.urls import include, path

from api.views import CategoryList, ProductList

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('products/', ProductList.as_view()),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
