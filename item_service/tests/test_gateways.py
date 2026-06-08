import pytest
import requests_mock
from items.gateways.divine_pride import DivinePrideGateway

@pytest.fixture
def gateway():
    # Setup test gateway
    gw = DivinePrideGateway()
    gw.api_key = "test_key"
    return gw

def test_get_item_by_id_success(gateway, requests_mock):
    # Arrange
    item_id = "1201"
    url = f"{gateway.base_url}{item_id}?apiKey=test_key&server=bRO"
    
    mock_response = {
        'id': 1201,
        'name': 'Faca Teste',
        'iconUrl': 'url',
        'attack': 100,
        'defense': 5,
        'location': 2
    }
    requests_mock.get(url, json=mock_response, status_code=200)

    # Act
    item, error = gateway.get_item_by_id(item_id)

    # Assert
    assert error is None
    assert item is not None
    assert item.name == 'Faca Teste'
    assert item.attack == 100

def test_get_item_by_id_not_found(gateway, requests_mock):
    # Arrange
    item_id = "99999"
    url = f"{gateway.base_url}{item_id}?apiKey=test_key&server=bRO"
    
    requests_mock.get(url, status_code=404)

    # Act
    item, error = gateway.get_item_by_id(item_id)

    # Assert
    assert item is None
    assert "Nenhum item com o ID '99999'" in error

def test_get_item_by_id_api_error(gateway, requests_mock):
    # Arrange
    item_id = "1201"
    url = f"{gateway.base_url}{item_id}?apiKey=test_key&server=bRO"
    
    requests_mock.get(url, status_code=500)

    # Act
    item, error = gateway.get_item_by_id(item_id)

    # Assert
    assert item is None
    assert "Erro desconhecido" in error
