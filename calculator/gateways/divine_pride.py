import requests
from django.conf import settings
from typing import Optional, Tuple, Dict
from calculator.domain.entities import Item
from calculator.gateways.interfaces import ItemGateway

class DivinePrideGateway(ItemGateway):
    def __init__(self):
        self.api_key = settings.DIVINE_PRIDE_API_KEY
        self.base_url = "https://www.divine-pride.net/api/database/Item/"

    def get_item_by_id(self, item_id: str) -> Tuple[Optional[Item], Optional[str]]:
        url = f"{self.base_url}{item_id}?apiKey={self.api_key}&server=bRO"
        
        try:
            response = requests.get(url, headers={'Accept-Language': 'pt-BR'})
            if response.status_code == 200:
                data = response.json()
                cleaned_data = self._clean_data(data)
                return Item.from_divine_pride_dict(cleaned_data), None
            elif response.status_code == 404:
                return None, f"Nenhum item com o ID '{item_id}' foi encontrado no Divine Pride."
            else:
                return None, "Erro desconhecido ao acessar a API do Divine Pride."
        except requests.RequestException:
            return None, "Erro de conexão ao acessar a API do Divine Pride."

    def _clean_data(self, data: Dict) -> Dict:
        """Trata as regras de negócio de tipos e locations específicas da API."""
        location = data.get('location', 0)
        item_type = data.get('type', 0)
        
        try: location = int(location) if location else 0
        except (ValueError, TypeError): location = 0
            
        if location == 0 and item_type == 5:
            try: location = int(data.get('subtype') or 0)
            except (ValueError, TypeError): pass
            
        data['location'] = location
        data['attack'] = int(data.get('attack') or 0)
        data['defense'] = int(data.get('defense') or 0)
        return data
