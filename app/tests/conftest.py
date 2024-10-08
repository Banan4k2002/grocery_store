from io import BytesIO

import pytest
from django.core.files.images import ImageFile
from PIL import Image
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from products.models import Category, Product, Subcategory
from shopping_cart.models import ShoppingCart


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def category():
    return Category.objects.create(title='Category 1', slug='category-1')


@pytest.fixture
def subcategory(category):
    return Subcategory.objects.create(
        title='Subcategory 1', slug='subcategory-1', category=category
    )


@pytest.fixture
def image():
    image = Image.new('RGB', (100, 100), color=(0, 0, 0))
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_file = ImageFile(image_io, name='temp_image.jpg')
    return image_file


@pytest.fixture
def product_1(subcategory, image):
    return Product.objects.create(
        title='Product 1',
        slug='product-1',
        subcategory=subcategory,
        price=100.00,
        image=image,
    )


@pytest.fixture
def product_2(subcategory, image):
    return Product.objects.create(
        title='Product 2',
        slug='product-2',
        subcategory=subcategory,
        price=200.00,
        image=image,
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser', password='password'
    )


@pytest.fixture
def shopping_cart_item_1(user, product_1):
    return ShoppingCart.objects.create(user=user, product=product_1)


@pytest.fixture
def shopping_cart_item_2(user, product_2):
    return ShoppingCart.objects.create(user=user, product=product_2)


@pytest.fixture
def token(user):

    token, _ = Token.objects.get_or_create(user=user)
    return token.key


@pytest.fixture
def user_client(token):

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client
