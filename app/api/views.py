from itertools import chain

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pagination import LimitPageNumberPagination
from api.serializers import (
    CategorySerializer,
    ProductSerializer,
    ShoppingCartListSerializer,
    ShoppingCartSerializer,
)
from products.models import Category, Product, Subcategory
from shopping_cart.models import ShoppingCart


class CategoryList(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        return list(chain(categories, subcategories))


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitPageNumberPagination

    @action(
        methods=('post', 'delete', 'patch'),
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,),
        serializer_class=ShoppingCartSerializer,
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )

        product = get_object_or_404(Product, pk=pk)
        cart = ShoppingCart.objects.filter(product=product, user=request.user)
        if cart.exists():

            if request.method == 'DELETE':
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            if request.method == 'PATCH':
                serializer = self.get_serializer(
                    cart.first(), data=request.data
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            data={'errors': 'Данного продукта нет в корзине'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=('delete',),
        detail=False,
        url_path='clear_shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def clear_shopping_cart(self, request):
        carts = ShoppingCart.objects.filter(user=request.user)
        carts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('get',),
        detail=False,
        url_path='get_shopping_cart',
        permission_classes=(IsAuthenticated,),
        serializer_class=ShoppingCartListSerializer,
    )
    def get_shopping_cart(self, request):
        carts = ShoppingCart.objects.filter(user=request.user)
        total_quantity = sum(cart.quantity for cart in carts)
        total_price = sum(cart.product.price * cart.quantity for cart in carts)

        serializer = self.get_serializer(
            {
                'products': carts,
                'total_quantity': total_quantity,
                'total_price': total_price,
            }
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
