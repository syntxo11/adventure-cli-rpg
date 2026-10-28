"""Player model and inventory effects."""

from __future__ import annotations

import random
from collections.abc import Mapping
from typing import Any

from config import MAX_ARMOR, PLAYER_START_ATTACK, PLAYER_START_HP
from models.character import Character
from models.item import (
    HEALING_POTION,
    ItemCode,
    ItemKind,
    item_kind,
    item_name,
    item_value,
    normalize_item_code,
)


class Player(Character):
    def __init__(self, name: str) -> None:
        super().__init__(name, max_hp=PLAYER_START_HP, attack=PLAYER_START_ATTACK)
        self.gold = 0
        self.inventory: list[ItemCode] = [HEALING_POTION]
        self.visited_rooms: set[int] = set()
        self.defeated_enemies: list[str] = []
        self.attack_bonus = 0
        self.armor = 0

    def add_item(self, item_code: ItemCode | str) -> None:
        code = normalize_item_code(item_code)
        if code is None:
            raise ValueError(f"Unknown item code: {item_code}")
        self.inventory.append(code)

    def get_total_attack(self) -> int:
        return self.attack + self.attack_bonus

    def reset_attack_bonus(self) -> None:
        self.attack_bonus = 0

    def add_armor(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Armor amount cannot be negative.")
        self.armor = min(MAX_ARMOR, self.armor + amount)

    def receive_hit(self, damage: int) -> int:
        """Apply armor first and return the damage that reached HP."""
        if damage < 0:
            raise ValueError("Damage cannot be negative.")

        blocked = min(self.armor, damage)
        self.armor -= blocked
        real_damage = damage - blocked
        self.take_damage(real_damage)
        return real_damage

    def use_item(self, item_code: ItemCode | str) -> str:
        code = normalize_item_code(item_code)
        if code is None or code not in self.inventory:
            return "You do not have this item."

        self.inventory.remove(code)
        kind = item_kind(code)
        value = item_value(code)
        name = item_name(code)

        match kind:
            case ItemKind.HEAL:
                self.heal(value)
                return f"You used {name}. +{value} HP."
            case ItemKind.RAGE:
                self.attack_bonus += value
                return f"You used {name}. +{value} attack for this fight."
            case ItemKind.ARMOR:
                self.add_armor(value)
                return f"You equipped {name}. +{value} armor."
            case ItemKind.WEAPON:
                self.attack += value
                return f"You equipped {name}. Permanent +{value} attack."
            case ItemKind.MYSTERY:
                return self.use_mystery_potion()
            case _:
                return "Nothing happened."

    def use_mystery_potion(self) -> str:
        effect = random.choice(("heal", "rage", "poison", "armor", "weakness"))

        match effect:
            case "heal":
                self.heal(20)
                return "Mystery Potion healed you. +20 HP."
            case "rage":
                self.attack_bonus += 5
                return "Mystery Potion made you stronger. +5 attack."
            case "poison":
                self.take_damage(8)
                return "Mystery Potion was poisoned. -8 HP."
            case "armor":
                self.add_armor(4)
                return "Mystery Potion hardened your skin. +4 armor."
            case "weakness":
                self.attack_bonus -= 2
                return "Mystery Potion made you weaker. -2 attack."
            case _:
                return "Nothing happened."

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "gold": self.gold,
                "inventory": [item.value for item in self.inventory],
                "visited_rooms": sorted(self.visited_rooms),
                "defeated_enemies": list(self.defeated_enemies),
                "attack_bonus": self.attack_bonus,
                "armor": self.armor,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Player":
        player = cls(str(data["name"]))
        player.max_hp = int(data["max_hp"])
        player.hp = int(data["hp"])
        player.attack = int(data["attack"])
        player.gold = int(data["gold"])

        inventory: list[ItemCode] = []
        for raw_code in data.get("inventory", []):
            code = normalize_item_code(str(raw_code))
            if code is not None:
                inventory.append(code)
        player.inventory = inventory

        player.visited_rooms = {int(room) for room in data.get("visited_rooms", [])}
        player.defeated_enemies = [str(name) for name in data.get("defeated_enemies", [])]
        player.attack_bonus = int(data.get("attack_bonus", 0))
        player.armor = int(data.get("armor", 0))
        return player
