import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from django.urls import reverse
from items.models import CachedItem

pytestmark = pytest.mark.django_db

# Carrega os cenários
scenarios('../features/search_item.feature')

@pytest.fixture
def api_client():
    from django.test import Client
    return Client()

@given(parsers.parse('que a API do Divine Pride esta operante e tem o item "{item_id}" chamado "{item_name}"'))
def mock_divine_pride_success(requests_mock, item_id, item_name):
    from django.conf import settings
    api_key = settings.DIVINE_PRIDE_API_KEY
    url = f"https://www.divine-pride.net/api/database/Item/{item_id}?apiKey={api_key}&server=bRO"
    mock_response = {
        'id': int(item_id),
        'name': item_name,
        'iconUrl': 'url',
        'attack': 100,
        'defense': 5,
        'location': 2
    }
    requests_mock.get(url, json=mock_response, status_code=200)

@given(parsers.parse('que a API do Divine Pride esta operante e NAO tem o item "{item_id}"'))
def mock_divine_pride_not_found(requests_mock, item_id):
    from django.conf import settings
    api_key = settings.DIVINE_PRIDE_API_KEY
    url = f"https://www.divine-pride.net/api/database/Item/{item_id}?apiKey={api_key}&server=bRO"
    requests_mock.get(url, status_code=404)

@when(parsers.parse('eu buscar pelo item de ID "{item_id}"'), target_fixture="response")
def buscar_item(api_client, item_id):
    url = reverse('search_item') + f"?q={item_id}"
    return api_client.get(url)

@then(parsers.parse('o sistema deve retornar sucesso e o nome do item "{item_name}"'))
def verificar_sucesso(response, item_name):
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert data['item']['name'] == item_name

@then(parsers.parse('o sistema deve retornar erro com a mensagem "{mensagem}"'))
def verificar_erro(response, mensagem):
    assert response.status_code == 404
    data = response.json()
    assert data['status'] == 'error'
    assert mensagem in data['message']
