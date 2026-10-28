import json

import pytest

from models.game_state import GameState
from models.item import IRON_SWORD
from models.player import Player
from utils.exceptions import SaveFileError
from utils.storage import load_game, save_game


def test_complete_game_state_roundtrip(tmp_path):
    path = tmp_path / "save.json"
    player = Player("Arthur")
    player.gold = 55
    player.hp = 21
    player.visited_rooms = {1, 2, 3, 4}
    player.add_item(IRON_SWORD)

    save_game(GameState(player, room_number=4, finished=False), path)
    restored = load_game(path)

    assert restored.room_number == 4
    assert restored.finished is False
    assert restored.player.to_dict() == player.to_dict()


def test_load_migrates_original_player_only_save(tmp_path):
    path = tmp_path / "legacy.json"
    player = Player("Legacy")
    player.visited_rooms = {1, 2, 3}
    path.write_text(json.dumps(player.to_dict()), encoding="utf-8")

    state = load_game(path)

    assert state.player.name == "Legacy"
    assert state.room_number == 3


def test_invalid_json_raises_domain_exception(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("not-json", encoding="utf-8")
    with pytest.raises(SaveFileError):
        load_game(path)


def test_missing_save_raises_domain_exception(tmp_path):
    with pytest.raises(SaveFileError, match="does not exist"):
        load_game(tmp_path / "missing.json")


def test_failed_save_does_not_overwrite_previous_save(tmp_path, monkeypatch):
    path = tmp_path / "save.json"
    path.write_text("previous save", encoding="utf-8")

    def fail_save(*args, **kwargs):
        raise OSError("disk error")

    monkeypatch.setattr("utils.storage.json.dump", fail_save)
    with pytest.raises(SaveFileError):
        save_game(GameState(Player("Arthur")), path)

    assert path.read_text(encoding="utf-8") == "previous save"
