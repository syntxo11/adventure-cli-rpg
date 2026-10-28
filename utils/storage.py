"""JSON persistence for complete game state."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import SAVE_VERSION
from models.game_state import GameState
from models.player import Player
from utils.exceptions import SaveFileError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAVE_PATH = PROJECT_ROOT / "data" / "save.json"


def save_game(state: GameState, path: Path = SAVE_PATH) -> None:
    """Persist the complete game state to JSON."""
    temp_path = path.with_name(path.name + ".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(state.to_dict(), file, indent=4)
        temp_path.replace(path)
    except OSError as error:
        temp_path.unlink(missing_ok=True)
        raise SaveFileError(f"Cannot save game: {error}") from error


def load_game(path: Path = SAVE_PATH) -> GameState:
    """Load current saves and migrate the original player-only save format."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data: dict[str, Any] = json.load(file)

        if "player" in data and "game" in data:
            version = int(data.get("version", SAVE_VERSION))
            if version > SAVE_VERSION:
                raise SaveFileError(
                    f"Save version {version} is newer than supported version {SAVE_VERSION}."
                )
            game_data = data["game"]
            return GameState(
                player=Player.from_dict(data["player"]),
                room_number=int(game_data.get("room_number", 0)),
                finished=bool(game_data.get("finished", False)),
                version=version,
            )

        # Legacy v0 format: the root object contains Player fields only.
        player = Player.from_dict(data)
        return GameState(
            player=player,
            room_number=max(player.visited_rooms, default=0),
            finished=False,
            version=SAVE_VERSION,
        )

    except FileNotFoundError as error:
        raise SaveFileError("Save file does not exist.") from error
    except SaveFileError:
        raise
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise SaveFileError(f"Cannot load save file: {error}") from error
