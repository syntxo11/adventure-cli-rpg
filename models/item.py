"""Typed item catalogue used by inventory and merchant systems."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ItemCode(str, Enum):
    HEALING_POTION = "healing_potion"
    RAGE_POTION = "rage_potion"
    MYSTERY_POTION = "mystery_potion"
    LEATHER_ARMOR = "leather_armor"
    IRON_ARMOR = "iron_armor"
    IRON_SWORD = "iron_sword"


class ItemKind(str, Enum):
    HEAL = "heal"
    RAGE = "rage"
    MYSTERY = "mystery"
    ARMOR = "armor"
    WEAPON = "weapon"


@dataclass(frozen=True, slots=True)
class Item:
    """Immutable item definition stored in the catalogue."""

    code: ItemCode
    name: str
    kind: ItemKind
    value: int
    price: int


ITEM_CATALOG: dict[ItemCode, Item] = {
    ItemCode.HEALING_POTION: Item(
        ItemCode.HEALING_POTION, "Healing Potion", ItemKind.HEAL, 15, 18
    ),
    ItemCode.RAGE_POTION: Item(
        ItemCode.RAGE_POTION, "Rage Potion", ItemKind.RAGE, 3, 22
    ),
    ItemCode.MYSTERY_POTION: Item(
        ItemCode.MYSTERY_POTION, "Mystery Potion", ItemKind.MYSTERY, 0, 15
    ),
    ItemCode.LEATHER_ARMOR: Item(
        ItemCode.LEATHER_ARMOR, "Leather Armor", ItemKind.ARMOR, 5, 25
    ),
    ItemCode.IRON_ARMOR: Item(
        ItemCode.IRON_ARMOR, "Iron Armor", ItemKind.ARMOR, 9, 45
    ),
    ItemCode.IRON_SWORD: Item(
        ItemCode.IRON_SWORD, "Iron Sword", ItemKind.WEAPON, 5, 25
    ),
}

SHOP_ITEMS: tuple[ItemCode, ...] = (
    ItemCode.HEALING_POTION,
    ItemCode.RAGE_POTION,
    ItemCode.MYSTERY_POTION,
    ItemCode.IRON_SWORD,
    ItemCode.IRON_ARMOR,
)

# Backwards-compatible names used throughout the game.
HEALING_POTION = ItemCode.HEALING_POTION
RAGE_POTION = ItemCode.RAGE_POTION
MYSTERY_POTION = ItemCode.MYSTERY_POTION
LEATHER_ARMOR = ItemCode.LEATHER_ARMOR
IRON_ARMOR = ItemCode.IRON_ARMOR
IRON_SWORD = ItemCode.IRON_SWORD


def normalize_item_code(item_code: ItemCode | str) -> ItemCode | None:
    try:
        return item_code if isinstance(item_code, ItemCode) else ItemCode(item_code)
    except ValueError:
        return None


def get_item(item_code: ItemCode | str) -> Item | None:
    code = normalize_item_code(item_code)
    return ITEM_CATALOG.get(code) if code is not None else None


def item_name(item_code: ItemCode | str) -> str:
    item = get_item(item_code)
    return item.name if item else str(item_code)


def item_kind(item_code: ItemCode | str) -> ItemKind | None:
    item = get_item(item_code)
    return item.kind if item else None


def item_value(item_code: ItemCode | str) -> int:
    item = get_item(item_code)
    return item.value if item else 0


def item_price(item_code: ItemCode | str) -> int:
    item = get_item(item_code)
    return item.price if item else 0
