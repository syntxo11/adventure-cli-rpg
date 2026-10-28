import models.player as player_module
from models.item import HEALING_POTION, IRON_SWORD, ItemCode, RAGE_POTION
from models.player import Player


def test_player_default_state():
    player = Player("Arthur")
    assert player.hp == 35
    assert player.attack == 7
    assert player.gold == 0
    assert player.inventory == [HEALING_POTION]


def test_armor_absorbs_damage_before_hp():
    player = Player("Arthur")
    player.armor = 5
    real_damage = player.receive_hit(8)
    assert real_damage == 3
    assert player.armor == 0
    assert player.hp == 32


def test_armor_can_block_full_hit():
    player = Player("Arthur")
    player.armor = 8
    real_damage = player.receive_hit(5)
    assert real_damage == 0
    assert player.armor == 3
    assert player.hp == 35


def test_healing_potion_is_consumed_and_heals():
    player = Player("Arthur")
    player.hp = 10
    message = player.use_item(HEALING_POTION)
    assert player.hp == 25
    assert HEALING_POTION not in player.inventory
    assert "Healing Potion" in message


def test_rage_bonus_can_be_reset():
    player = Player("Arthur")
    player.add_item(RAGE_POTION)
    player.use_item(RAGE_POTION)
    assert player.get_total_attack() == 10
    player.reset_attack_bonus()
    assert player.get_total_attack() == 7


def test_weapon_permanently_increases_base_attack():
    player = Player("Arthur")
    player.add_item(IRON_SWORD)
    player.use_item(IRON_SWORD)
    assert player.attack == 12
    assert player.get_total_attack() == 12


def test_mystery_poison_can_kill_player(monkeypatch):
    player = Player("Arthur")
    player.hp = 5
    player.inventory = [ItemCode.MYSTERY_POTION]
    monkeypatch.setattr(player_module.random, "choice", lambda _: "poison")
    player.use_item(ItemCode.MYSTERY_POTION)
    assert player.hp == 0
    assert not player.is_alive()


def test_player_serialization_roundtrip():
    player = Player("Arthur")
    player.gold = 44
    player.visited_rooms = {1, 2, 3}
    player.add_item(IRON_SWORD)
    restored = Player.from_dict(player.to_dict())
    assert restored.to_dict() == player.to_dict()
