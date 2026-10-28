import pytest

from models.character import Character


def test_character_starts_with_full_health():
    character = Character("Hero", max_hp=30, attack=5)
    assert character.hp == 30
    assert character.is_alive()


def test_damage_cannot_reduce_hp_below_zero():
    character = Character("Hero", max_hp=10, attack=5)
    character.take_damage(50)
    assert character.hp == 0
    assert not character.is_alive()


def test_healing_cannot_exceed_max_hp():
    character = Character("Hero", max_hp=30, attack=5)
    character.take_damage(20)
    character.heal(100)
    assert character.hp == 30


def test_negative_damage_is_rejected():
    character = Character("Hero", max_hp=30, attack=5)
    with pytest.raises(ValueError):
        character.take_damage(-1)
