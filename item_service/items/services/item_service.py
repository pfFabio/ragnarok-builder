from typing import Optional, Tuple
from items.domain.entities import Item
from items.gateways.interfaces import ItemGateway
from items.models import CachedItem

class ItemService:
    def __init__(self, gateway: ItemGateway):
        self.gateway = gateway

    def _get_from_db(self, item_id: str) -> Optional[Item]:
        try:
            cached = CachedItem.objects.get(item_id=item_id)
            return Item(
                id=cached.item_id,
                name=cached.name,
                icon_url=cached.icon_url,
                attack=cached.attack,
                defense=cached.defense,
                str_bonus=cached.str_bonus,
                agi_bonus=cached.agi_bonus,
                vit_bonus=cached.vit_bonus,
                int_bonus=cached.int_bonus,
                dex_bonus=cached.dex_bonus,
                luk_bonus=cached.luk_bonus
            )
        except CachedItem.DoesNotExist:
            return None

    def _save_to_db(self, item: Item):
        CachedItem.objects.update_or_create(
            item_id=item.id,
            defaults={
                'name': item.name,
                'icon_url': item.icon_url,
                'attack': item.attack,
                'defense': item.defense,
                'str_bonus': item.str_bonus,
                'agi_bonus': item.agi_bonus,
                'vit_bonus': item.vit_bonus,
                'int_bonus': item.int_bonus,
                'dex_bonus': item.dex_bonus,
                'luk_bonus': item.luk_bonus
            }
        )

    def get_item(self, item_id: str) -> Tuple[Optional[Item], Optional[str]]:
        if not item_id.isdigit():
            return None, "O ID do item deve ser numérico."

        cached_item = self._get_from_db(item_id)
        if cached_item:
            return cached_item, None

        item, error = self.gateway.get_item_by_id(item_id)
        if item:
            self._save_to_db(item)
        
        return item, error
