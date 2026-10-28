"""Serializable game-state container."""

from __future__ import annotations

from dataclasses import dataclass

from config import SAVE_VERSION
from models.player import Player


@dataclass(slots=True)
class GameState:
    player: Player
    room_number: int = 0
    finished: bool = False
    version: int = SAVE_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "game": {
                "room_number": self.room_number,
                "finished": self.finished,
            },
            "player": self.player.to_dict(),
        }
