"""Base character model shared by the player and enemies."""

from __future__ import annotations


class Character:
    """Represent a combat character with health and attack statistics."""

    def __init__(self, name: str, max_hp: int, attack: int) -> None:
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> None:
        if damage < 0:
            raise ValueError("Damage cannot be negative.")
        self.hp = max(0, self.hp - damage)

    def heal(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Healing amount cannot be negative.")
        self.hp = min(self.max_hp, self.hp + amount)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
        }
