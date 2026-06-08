from abc import ABC, abstractmethod
from typing import Optional, Tuple
from items.domain.entities import Item

class ItemGateway(ABC):
    @abstractmethod
    def get_item_by_id(self, item_id: str) -> Tuple[Optional[Item], Optional[str]]:
        pass
