import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize('client_type', ('client', 'user_client'))
def test_get_categories_list(request, client_type, category, subcategory):
    url = reverse('category-list')
    client = request.getfixturevalue(client_type)
    response = client.get(url)

    assert len(response.data['results']) == 2
    assert response.data['results'][0]['title'] == category.title
    assert response.data['results'][1]['title'] == subcategory.title
    assert response.status_code == status.HTTP_200_OK
