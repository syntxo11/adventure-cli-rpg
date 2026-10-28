"""Room progression, enemy factories, and random exploration events."""

from __future__ import annotations

import random
from typing import Literal

from config import FINAL_BOSS_ROOM, MERCHANT_ROOM, MINI_BOSS_ROOMS
from models.boss import Boss
from models.enemy import Enemy
from models.item import HEALING_POTION, MYSTERY_POTION, RAGE_POTION, ItemCode

EventType = Literal[
    "enemy",
    "empty",
    "treasure",
    "trap",
    "potion",
    "merchant",
    "mini_boss",
    "final_boss",
]


def normal_event() -> EventType:
    """Return a weighted random exploration event."""
    events: tuple[EventType, ...] = (
        "enemy",
        "enemy",
        "enemy",
        "empty",
        "empty",
        "treasure",
        "trap",
        "potion",
        "merchant",
    )
    return random.choice(events)


def stage_event(room_number: int) -> EventType:
    """Return the scripted event for milestone rooms, otherwise a random event."""
    if room_number in MINI_BOSS_ROOMS:
        return "mini_boss"
    if room_number == MERCHANT_ROOM:
        return "merchant"
    if room_number == FINAL_BOSS_ROOM:
        return "final_boss"
    return normal_event()


def create_enemy() -> Enemy:
    enemies = (
        Enemy(
            name="Goblin",
            max_hp=16,
            attack=4,
            gold_reward=10,
            dialogues=(
                "You smell like fear.",
                "Tiny hero, big mistake.",
                "Your gold will look better in my pocket.",
            ),
        ),
        Enemy(
            name="Skeleton",
            max_hp=20,
            attack=5,
            gold_reward=14,
            dialogues=(
                "Another lost soul...",
                "I remember the sound of fire.",
                "Your bones will join mine.",
            ),
        ),
        Enemy(
            name="Dark Rat",
            max_hp=12,
            attack=3,
            gold_reward=7,
            dialogues=(
                "Hssssssss...",
                "Small teeth. Deep wounds.",
                "The dark feeds us all.",
            ),
        ),
    )
    return random.choice(enemies)


def create_mini_boss(stage_number: int) -> Boss:
    names = {1: "Gate Butcher", 2: "Bone Knight"}
    return Boss(
        name=names.get(stage_number, "Castle Guardian"),
        max_hp=38 + stage_number * 6,
        attack=7 + stage_number,
        gold_reward=35 + stage_number * 10,
        dialogues=(
            "No one passes this gate.",
            "Your revenge ends here.",
            "I will hang your sword above my door.",
        ),
        enrage_threshold=0.4,
        enrage_bonus=2,
    )


def create_final_boss() -> Boss:
    return Boss(
        name="Crimson King",
        max_hp=70,
        attack=12,
        gold_reward=120,
        dialogues=(
            "I remember your family.",
            "You came all this way just to die here?",
            "Your revenge is a child's dream.",
            "Kneel, survivor.",
        ),
        enrage_threshold=0.5,
        enrage_bonus=3,
    )


def random_potion() -> ItemCode:
    potions = (
        HEALING_POTION,
        HEALING_POTION,
        RAGE_POTION,
        RAGE_POTION,
        MYSTERY_POTION,
    )
    return random.choice(potions)


def random_exploration_lines() -> list[str]:
    lines = (
        "Darkness fills the corridor.",
        "The air smells like dust and blood.",
        "Your footsteps echo through the empty hall.",
        "A cold wind passes through the room.",
        "The torches flicker for no reason.",
        "Something scratches the wall nearby.",
        "You hear a distant whisper.",
        "The floor feels unstable under your feet.",
    )
    return random.sample(lines, 2)


def empty_room_text() -> str:
    lines = (
        "The room is empty, but something feels wrong.",
        "Only broken furniture remains here.",
        "You find old scratches on the stone floor.",
        "For a moment, you hear breathing. Then silence.",
        "A torn banner moves in the cold air.",
    )
    return random.choice(lines)
