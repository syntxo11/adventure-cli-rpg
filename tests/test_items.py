from models.item import IRON_ARMOR, ItemKind, get_item, item_name, item_price


def test_catalog_returns_typed_item_definition():
    item = get_item(IRON_ARMOR)
    assert item is not None
    assert item.kind is ItemKind.ARMOR
    assert item.value == 9


def test_item_helpers_accept_string_codes():
    assert item_name("iron_armor") == "Iron Armor"
    assert item_price("iron_armor") == 45
