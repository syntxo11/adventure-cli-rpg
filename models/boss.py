"""Boss enemy with a second combat phase."""

from __future__ import annotations

from collections.abc import Sequence

from models.enemy import Enemy


class Boss(Enemy):
    """Enemy that becomes enraged after falling below a HP threshold."""

    def __init__(
        self,
        name: str,
        max_hp: int,
        attack: int,
        gold_reward: int,
        dialogues: Sequence[str],
        *,
        enrage_threshold: float = 0.5,
        enrage_bonus: int = 2,
    ) -> None:
        super().__init__(name, max_hp, attack, gold_reward, dialogues)
        self.enrage_threshold = enrage_threshold
        self.enrage_bonus = enrage_bonus
        self.enraged = False

    def take_damage(self, damage: int) -> None:
        super().take_damage(damage)
        if self.is_alive() and self.hp <= self.max_hp * self.enrage_threshold:
            self.enraged = True

    def get_total_attack(self) -> int:
        return self.attack + (self.enrage_bonus if self.enraged else 0)

    @property
    def phase_name(self) -> str:
        return "ENRAGED" if self.enraged else "NORMAL"
