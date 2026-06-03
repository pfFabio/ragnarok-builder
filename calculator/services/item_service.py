from typing import Optional, Tuple
from calculator.domain.entities import Item
from calculator.gateways.interfaces import ItemGateway

class ItemCache:
    """Singleton cache para itens."""
    _instance = None
    _cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ItemCache, cls).__new__(cls)
        return cls._instance

    def get(self, item_id: str) -> Optional[Item]:
        return self._cache.get(item_id)

    def set(self, item_id: str, item: Item):
        self._cache[item_id] = item

class ItemService:
    def __init__(self, gateway: ItemGateway, cache: ItemCache):
        self.gateway = gateway
        self.cache = cache

    def get_item(self, item_id: str) -> Tuple[Optional[Item], Optional[str]]:
        if not item_id.isdigit():
            return None, "O ID do item deve ser numérico."

        cached_item = self.cache.get(item_id)
        if cached_item:
            return cached_item, None

        item, error = self.gateway.get_item_by_id(item_id)
        if item:
            self.cache.set(item_id, item)
        
        return item, error
