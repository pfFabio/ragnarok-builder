import pytest
from items.services.item_service import ItemService
from items.domain.entities import Item
from items.models import CachedItem

class MockGateway:
    def get_item_by_id(self, item_id):
        if item_id == "1201":
            item = Item(id="1201", name="Mock Faca", icon_url="url", attack=50, defense=0, location=2)
            return item, None
        return None, "Item não encontrado"

@pytest.fixture
def service():
    return ItemService(gateway=MockGateway())

@pytest.mark.django_db
def test_get_item_not_in_cache(service):
    # Act
    item, error = service.get_item("1201")

    # Assert
    assert error is None
    assert item is not None
    assert item.name == "Mock Faca"
    
    # Check if it was saved in cache
    cached = CachedItem.objects.filter(item_id="1201").first()
    assert cached is not None
    assert cached.name == "Mock Faca"

@pytest.mark.django_db
def test_get_item_from_cache(service):
    # Arrange: Save directly to DB to bypass gateway
    CachedItem.objects.create(
        item_id="1201",
        name="Cached Faca",
        icon_url="url",
        attack=150,
        defense=0
    )

    # Act
    item, error = service.get_item("1201")

    # Assert
    assert error is None
    assert item.name == "Cached Faca" # Should come from cache, not Mock Faca
    assert item.attack == 150

@pytest.mark.django_db
def test_get_item_not_found(service):
    # Act
    item, error = service.get_item("9999")

    # Assert
    assert item is None
    assert "Item não encontrado" in error
