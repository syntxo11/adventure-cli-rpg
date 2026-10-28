import core.combat as combat
from models.boss import Boss
from models.enemy import Enemy
from models.player import Player


def test_damage_bonus_applies_to_high_attack():
    player = Player("Arthur")
    player.attack = 8
    assert combat.damage_of(player) == 10


def test_damage_bonus_not_applied_below_threshold():
    enemy = Enemy("Rat", max_hp=10, attack=4, gold_reward=1, dialogues=("hiss",))
    assert combat.damage_of(enemy) == 4


def test_enraged_boss_damage_uses_phase_bonus():
    boss = Boss(
        "Boss",
        max_hp=20,
        attack=8,
        gold_reward=1,
        dialogues=("x",),
        enrage_bonus=3,
    )
    boss.take_damage(10)
    assert combat.damage_of(boss) == 13


def test_escape_chance_depends_on_health(monkeypatch):
    player = Player("Arthur")
    monkeypatch.setattr(combat.random, "randint", lambda _a, _b: 30)
    escaped, chance = combat.can_escape(player)
    assert chance == 40
    assert escaped is True

    player.hp = 10
    escaped, chance = combat.can_escape(player)
    assert chance == 15
    assert escaped is False
