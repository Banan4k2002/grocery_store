from itertools import chain

from rest_framework.generics import ListAPIView

from api.pagination import LimitPageNumberPagination
from api.serializers import CategorySerializer, ProductSerializer
from products.models import Category, Product, Subcategory


class CategoryList(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        return list(chain(categories, subcategories))


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitPageNumberPagination
