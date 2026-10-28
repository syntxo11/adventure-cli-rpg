"""Enemy model."""

from __future__ import annotations

import random
from collections.abc import Sequence

from models.character import Character


class Enemy(Character):
    def __init__(
        self,
        name: str,
        max_hp: int,
        attack: int,
        gold_reward: int,
        dialogues: Sequence[str],
    ) -> None:
        super().__init__(name, max_hp, attack)
        self.gold_reward = gold_reward
        self.dialogues = tuple(dialogues)

    def get_dialogue(self) -> str:
        return random.choice(self.dialogues)
