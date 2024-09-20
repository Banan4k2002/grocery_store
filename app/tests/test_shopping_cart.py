from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from shopping_cart.models import ShoppingCart


def test_add_product_to_cart(user_client, user, product_1):
    url = reverse('product-shopping-cart', kwargs={'pk': product_1.pk})
    response = user_client.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingCart.objects.filter(user=user, product=product_1).exists()


def test_add_product_to_cart_exists(user_client, shopping_cart_item_1):
    product = shopping_cart_item_1.product
    url = reverse('product-shopping-cart', kwargs={'pk': product.pk})
    response = user_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Продукт уже добавлен в корзину' in response.data['errors']


def test_change_product_quantity(user_client, shopping_cart_item_1):
    url = reverse(
        'product-shopping-cart', kwargs={'pk': shopping_cart_item_1.product.pk}
    )
    data = {'quantity': 5}
    response = user_client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    shopping_cart_item_1.refresh_from_db()
    assert shopping_cart_item_1.quantity == data['quantity']


def test_change_product_quantity_non_exists(user_client, product_1):
    url = reverse('product-shopping-cart', kwargs={'pk': product_1.pk})
    data = {'quantity': 5}
    response = user_client.patch(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Данного продукта нет в корзине' in response.data['errors']


def test_remove_product_from_cart(user_client, shopping_cart_item_1):
    url = reverse(
        'product-shopping-cart', kwargs={'pk': shopping_cart_item_1.product.pk}
    )
    response = user_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not ShoppingCart.objects.filter(pk=shopping_cart_item_1.pk).exists()


def test_remove_product_from_cart_non_exists(user_client, product_1):
    url = reverse('product-shopping-cart', kwargs={'pk': product_1.pk})
    response = user_client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Данного продукта нет в корзине' in response.data['errors']


def test_cart_list(user_client, shopping_cart_item_1, shopping_cart_item_2):
    url = reverse('product-get-shopping-cart')
    response = user_client.get(url)

    total_quantity = (
        shopping_cart_item_1.quantity + shopping_cart_item_2.quantity
    )
    total_price = (
        shopping_cart_item_1.quantity * shopping_cart_item_1.product.price
        + shopping_cart_item_2.quantity * shopping_cart_item_2.product.price
    )

    assert response.status_code == status.HTTP_200_OK
    assert 'products' in response.data
    assert 'total_quantity' in response.data
    assert 'total_price' in response.data
    assert response.data['total_quantity'] == total_quantity
    assert Decimal(response.data['total_price']) == total_price


def test_cart_clear(
    user_client, shopping_cart_item_1, shopping_cart_item_2, user
):
    url = reverse('product-clear-shopping-cart')
    response = user_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not ShoppingCart.objects.filter(user=user).exists()


@pytest.mark.parametrize(
    'reverse_path, method, kwargs',
    (
        ('product-shopping-cart', 'post', {'pk': 1}),
        ('product-shopping-cart', 'patch', {'pk': 1}),
        ('product-shopping-cart', 'delete', {'pk': 1}),
        ('product-get-shopping-cart', 'get', {}),
        ('product-clear-shopping-cart', 'delete', {}),
    ),
)
def test_shopping_cart_not_auth(
    client, product_1, reverse_path, method, kwargs
):
    url = reverse(reverse_path, kwargs=kwargs)
    if method == 'get':
        response = client.get(url)
    elif method == 'post':
        response = client.post(url)
    elif method == 'patch':
        data = {'quantity': 5}
        response = client.patch(url, data=data)
    elif method == 'delete':
        response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize('method', ('post', 'patch', 'delete'))
def test_product_not_exists(user_client, method):
    url = reverse('product-shopping-cart', kwargs={'pk': 1})
    if method == 'post':
        response = user_client.post(url)
    elif method == 'patch':
        response = user_client.patch(url, data={'quantity': 5})
    elif method == 'delete':
        response = user_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
