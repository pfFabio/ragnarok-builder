from dataclasses import dataclass, field
from typing import Dict

@dataclass(frozen=True)
class Item:
    id: int
    name: str
    icon_url: str
    attack: int = 0
    defense: int = 0
    str_bonus: int = 0
    agi_bonus: int = 0
    vit_bonus: int = 0
    int_bonus: int = 0
    dex_bonus: int = 0
    luk_bonus: int = 0
    location: int = 0

    @classmethod
    def from_divine_pride_dict(cls, data: Dict):
        """Factory method para criar um Item a partir do dicionário da API Divine Pride."""
        stats = data.get('stat', {})
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            icon_url=f"https://static.divine-pride.net/images/items/item/{data.get('id')}.png",
            attack=data.get('attack', 0),
            defense=data.get('defense', 0),
            str_bonus=stats.get('str', 0),
            agi_bonus=stats.get('agi', 0),
            vit_bonus=stats.get('vit', 0),
            int_bonus=stats.get('int', 0),
            dex_bonus=stats.get('dex', 0),
            luk_bonus=stats.get('luk', 0),
            location=data.get('location', 0)
        )
