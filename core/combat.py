"""Turn-based combat rules."""

from __future__ import annotations

import random
from typing import Protocol

from config import (
    ESCAPE_CHANCE_HIGH_HP,
    ESCAPE_CHANCE_LOW_HP,
    ESCAPE_CHANCE_MEDIUM_HP,
    MISS_CHANCE_PERCENT,
)
from core.inventory import choose_inventory_item
from models.boss import Boss
from models.enemy import Enemy
from models.player import Player
from utils.exceptions import GameOverError
from utils.ui import (
    BLUE,
    GREEN,
    MUTED,
    RED,
    YELLOW,
    choices,
    clear,
    info_box,
    msg,
    pause,
    say,
    title,
    victory_title,
)


class Attacker(Protocol):
    attack: int


def damage_of(attacker: Attacker) -> int:
    """Calculate attack damage including the high-attack bonus."""
    total_attack = (
        attacker.get_total_attack()  # type: ignore[attr-defined]
        if hasattr(attacker, "get_total_attack")
        else attacker.attack
    )
    bonus = 2 if total_attack >= 8 else 0
    return total_attack + bonus


def can_escape(player: Player) -> tuple[bool, int]:
    hp_percent = player.hp / player.max_hp
    if hp_percent > 0.6:
        chance = ESCAPE_CHANCE_HIGH_HP
    elif hp_percent > 0.3:
        chance = ESCAPE_CHANCE_MEDIUM_HP
    else:
        chance = ESCAPE_CHANCE_LOW_HP
    return random.randint(1, 100) <= chance, chance


def show_battle(player: Player, enemy: Enemy) -> None:
    title(f"{player.name} VS {enemy.name}", RED if isinstance(enemy, Boss) else None)

    lines = [
        f"{player.name} HP: {player.hp} / {player.max_hp}",
        f"Armor: {player.armor}",
        f"{enemy.name} HP: {enemy.hp} / {enemy.max_hp}",
        f"Your attack: {player.get_total_attack()}",
    ]
    if isinstance(enemy, Boss):
        lines.append(f"Boss phase: {enemy.phase_name}")
    info_box(lines)
    choices(("[1] Attack", "[2] Use item", "[3] Run away"))


def enemy_attack(player: Player, enemy: Enemy) -> None:
    if random.randint(1, 100) <= MISS_CHANCE_PERCENT:
        msg(f"{enemy.name} missed.", MUTED)
        return

    enemy_damage = damage_of(enemy)
    real_damage = player.receive_hit(enemy_damage)
    if real_damage == 0:
        msg("Your armor blocked the hit.", BLUE)
    else:
        msg(f"{enemy.name} attacks you for {real_damage} damage.", RED)


def start_fight(player: Player, enemy: Enemy) -> bool:
    clear()
    if isinstance(enemy, Boss):
        title("BOSS ROOM", RED)
        say("The throne room feels cold.", code=RED)
        say("Heavy steps echo somewhere nearby.", code=RED)
        print(f"\n{enemy.name}:")
        say(enemy.get_dialogue(), delay=0.07, prefix="", code=RED)
        say("The monster slowly rises.", code=RED)
    else:
        title("ENEMY")
        say(f"A {enemy.name} blocks your path.")
        print(f"\n{enemy.name}:")
        say(enemy.get_dialogue(), delay=0.05, prefix="")
        say("Its eyes glow in the darkness.")
    pause()

    while enemy.is_alive() and player.is_alive():
        clear()
        show_battle(player, enemy)
        choice = input("\nChoose option: ")

        match choice:
            case "1":
                was_enraged = isinstance(enemy, Boss) and enemy.enraged
                if random.randint(1, 100) <= MISS_CHANCE_PERCENT:
                    msg("You missed.", MUTED)
                else:
                    damage = damage_of(player)
                    enemy.take_damage(damage)
                    msg(f"You attack {enemy.name} for {damage} damage.", YELLOW)

                if isinstance(enemy, Boss) and enemy.enraged and not was_enraged:
                    msg(f"{enemy.name} enters an enraged phase!", RED)

                if enemy.is_alive():
                    enemy_attack(player, enemy)

            case "2":
                selected_item = choose_inventory_item(player)
                if selected_item is not None:
                    say(player.use_item(selected_item), code=GREEN)
                    if not player.is_alive():
                        raise GameOverError("The potion was your last mistake.")

            case "3":
                if isinstance(enemy, Boss):
                    say("You cannot run away from a boss!", code=RED)
                else:
                    escaped, chance = can_escape(player)
                    if escaped:
                        msg(f"You escaped. Chance was {chance}%.", BLUE)
                        player.reset_attack_bonus()
                        pause()
                        return False
                    msg(f"Escape failed. Chance was {chance}%.", RED)
                    enemy_attack(player, enemy)

            case _:
                msg("Wrong option.", RED)

        pause()

    if not player.is_alive():
        player.reset_attack_bonus()
        raise GameOverError("Your body falls onto the cold stone floor.")

    victory_title()
    say(f"You defeated {enemy.name}!", code=GREEN)
    msg(f"You gained {enemy.gold_reward} gold.", YELLOW)
    player.gold += enemy.gold_reward
    player.defeated_enemies.append(enemy.name)
    player.reset_attack_bonus()
    pause()
    return True
