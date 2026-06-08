import pytest
from items.domain.entities import Item

def test_create_item_from_divine_pride_dict():
    # Arrange
    data = {
        'id': 1201,
        'name': 'Faca',
        'iconUrl': 'https://static.divine-pride.net/images/items/item/1201.png',
        'attack': 100,
        'defense': 0,
        'stat': {
            'str': 0,
            'agi': 0,
            'vit': 0,
            'int': 0,
            'dex': 0,
            'luk': 0,
        },
        'location': 2,
    }

    # Act
    item = Item.from_divine_pride_dict(data)

    # Assert
    assert item.id == 1201
    assert item.name == "Faca"
    assert item.attack == 100
    assert item.defense == 0
    assert item.location == 2
    assert item.icon_url == "https://static.divine-pride.net/images/items/item/1201.png"

def test_create_item_with_bonus():
    # Arrange
    data = {
        'id': 1202,
        'name': 'Espada',
        'iconUrl': '',
        'attack': 150,
        'defense': 10,
        'stat': {
            'str': 5,
            'agi': 2,
            'vit': 1,
            'int': 0,
            'dex': 3,
            'luk': 4,
        },
        'location': 2,
    }

    # Act
    item = Item.from_divine_pride_dict(data)

    # Assert
    assert item.str_bonus == 5
    assert item.agi_bonus == 2
    assert item.vit_bonus == 1
    assert item.dex_bonus == 3
    assert item.luk_bonus == 4
