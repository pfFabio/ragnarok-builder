import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse

from calculator.domain.entities import Item
from calculator.services.item_service import ItemService, ItemCache
from calculator.gateways.divine_pride import DivinePrideGateway
from calculator.models import Build

class ItemDomainTest(TestCase):
    def test_item_creation_from_dict(self):
        data = {
            'id': 1201,
            'name': 'Sword',
            'attack': 100,
            'stat': {'str': 5},
            'location': 2
        }
        item = Item.from_divine_pride_dict(data)
        self.assertEqual(item.id, 1201)
        self.assertEqual(item.str_bonus, 5)

class ItemServiceTest(TestCase):
    def setUp(self):
        self.mock_gateway = MagicMock()
        self.cache = ItemCache()
        # Limpa o cache entre os testes se necessário (Singleton)
        ItemCache._cache = {}
        self.service = ItemService(gateway=self.mock_gateway, cache=self.cache)

    def test_get_item_calls_gateway_and_caches(self):
        item_data = Item(id=1, name='Test', icon_url='')
        self.mock_gateway.get_item_by_id.return_value = (item_data, None)
        
        item, error = self.service.get_item('1')
        
        self.assertEqual(item, item_data)
        self.mock_gateway.get_item_by_id.assert_called_once_with('1')
        self.assertEqual(self.cache.get('1'), item_data)

    def test_get_item_returns_cached_value(self):
        item_data = Item(id=1, name='Cached', icon_url='')
        self.cache.set('1', item_data)
        
        item, error = self.service.get_item('1')
        
        self.assertEqual(item, item_data)
        self.mock_gateway.get_item_by_id.assert_not_called()

class SearchItemFeatureTest(TestCase):
    """BDD-style Integration Test for Search Item feature."""
    
    def setUp(self):
        self.client = Client()

    @patch('calculator.services.item_service.ItemService.get_item')
    def test_user_searches_item_by_id_successfully(self, mock_get_item):
        # Scenario: User searches for item 1201
        item = Item(id=1201, name='Espada de Teste', icon_url='url', attack=50)
        mock_get_item.return_value = (item, None)
        
        response = self.client.get(reverse('search_item'), {'q': '1201'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Espada de Teste')
        self.assertContains(response, '50')

    def test_user_searches_item_with_invalid_query(self):
        # Scenario: User searches with non-numeric ID
        response = self.client.get(reverse('search_item'), {'q': 'abc'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'O ID do item deve ser numérico')

class BuildFeatureTest(TestCase):
    """Tests for Build Saving and Loading."""
    
    def setUp(self):
        self.client = Client()

    def test_save_and_list_build(self):
        build_data = {
            'nome': 'Minha Build',
            'classe': 'Algoz',
            'str': 99
        }
        # Save
        response = self.client.post(
            reverse('save_build'),
            data=json.dumps(build_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        build_id = response.json()['build_id']
        
        # List
        response = self.client.get(reverse('list_builds'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(b['nome'] == 'Minha Build' for b in response.json()['builds']))
        
        # Load
        response = self.client.get(reverse('load_build', args=[build_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['build']['nome'], 'Minha Build')
