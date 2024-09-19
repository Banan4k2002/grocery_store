import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize('client_type', ('client', 'user_client'))
@pytest.mark.django_db
def test_get_product_list(request, client_type, product_1, product_2):
    url = reverse('product-list')
    client = request.getfixturevalue(client_type)
    response = client.get(url)
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['title'] == product_1.title
    assert response.data['results'][1]['title'] == product_2.title
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('client_type', ('client', 'user_client'))
@pytest.mark.django_db
def test_get_product_detail(request, client_type, product_1):
    url = reverse('product-detail', kwargs={'pk': product_1.pk})
    client = request.getfixturevalue(client_type)
    response = client.get(url)
    assert response.data['title'] == product_1.title
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('client_type', ('client', 'user_client'))
@pytest.mark.django_db
def test_get_product_detail_not_exist(request, client_type):
    url = reverse('product-detail', kwargs={'pk': 1})
    client = request.getfixturevalue(client_type)
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
