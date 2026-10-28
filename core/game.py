"""Main application controller for ADVENTURE."""

from __future__ import annotations

import random
import time

from config import FINAL_BOSS_ROOM, MINI_BOSS_ROOMS, TOTAL_ROOMS
from core.combat import start_fight
from core.events import (
    create_enemy,
    create_final_boss,
    create_mini_boss,
    empty_room_text,
    random_exploration_lines,
    random_potion,
    stage_event,
)
from core.inventory import choose_inventory_item
from models.game_state import GameState
from models.item import SHOP_ITEMS, ItemCode, item_name, item_price
from models.player import Player
from utils.exceptions import GameOverError, InvalidHeroNameError, SaveFileError
from utils.storage import load_game, save_game
from utils.ui import (
    ADVENTURE_LOGO,
    BLUE,
    CYAN,
    GREEN,
    MUTED,
    PURPLE,
    RED,
    YELLOW,
    choices,
    clear,
    color,
    info_box,
    msg,
    pause,
    say,
    title,
)
from utils.validators import validate_hero_name


class Game:
    def __init__(self) -> None:
        self.player: Player | None = None
        self.room_number = 0
        self.finished = False

    def run(self) -> None:
        while True:
            clear()
            print(color(ADVENTURE_LOGO.strip(), CYAN))
            print(color("# a dark journey begins".center(60), MUTED))
            choices(("[1] Start", "[2] Load", "[3] Info", "[4] Quit"))
            choice = input("\nChoose option: ")

            match choice:
                case "1":
                    self.start_new()
                    self.play()
                case "2":
                    self.load()
                    if self.player is not None:
                        self.play()
                case "3":
                    self.show_info()
                case "4":
                    msg("Goodbye!", MUTED)
                    break
                case _:
                    msg("Wrong option.", RED)
                    pause()

    def start_new(self) -> None:
        while True:
            clear()
            title("CREATE HERO", CYAN)
            msg("Enter the name of the one who survived.")
            msg("Name must be 3-15 characters.")
            msg("Allowed: letters, digits, underscore.")
            name = input("\nEnter hero name: ")

            try:
                validate_hero_name(name)
                self.player = Player(name)
                self.room_number = 0
                self.finished = False
                self.show_story(name)
                return
            except InvalidHeroNameError as error:
                msg(f"Error: {error}", RED)
                pause()

    def show_story(self, hero_name: str) -> None:
        clear()
        title("PROLOGUE", PURPLE)
        story_lines = (
            f"Long ago, {hero_name}'s village lived in peace.",
            "But one night, the Crimson King's army came.",
            "Fire covered the village.",
            "By morning, nothing remained.",
            "Your family was gone.",
            "You survived.",
            "Years passed.",
            "You trained. You searched. You waited.",
            "At last, you found his trail.",
            "The gates of the dark castle stand before you.",
        )
        for text in story_lines:
            say(text, delay=0.025, code=PURPLE)
            time.sleep(0.12)
        pause()

    def play(self) -> None:
        while self.player is not None and self.player.is_alive() and not self.finished:
            clear()
            title("ADVENTURE", CYAN)
            info_box(
                (
                    f"Hero: {self.player.name}",
                    f"Room: {self.room_number} / {TOTAL_ROOMS}",
                    f"HP: {self.player.hp} / {self.player.max_hp}",
                    f"Armor: {self.player.armor}",
                    f"Attack: {self.player.attack}",
                    f"Temporary attack bonus: {self.player.attack_bonus}",
                    f"Gold: {self.player.gold}",
                    f"Inventory: {self.inventory_text()}",
                )
            )
            choices(("[1] Explore", "[2] Stats", "[3] Inventory", "[4] Save", "[5] Exit"))
            choice = input("\nChoose option: ")

            try:
                match choice:
                    case "1":
                        self.explore()
                    case "2":
                        self.show_stats()
                    case "3":
                        self.open_inventory()
                    case "4":
                        self.save()
                    case "5":
                        break
                    case _:
                        msg("Wrong option.", RED)
                        pause()
            except GameOverError as error:
                clear()
                title("GAME OVER", RED)
                say(str(error), code=RED)
                say("The castle becomes silent once again.", code=RED)
                say("Revenge will remain unfinished.", code=RED)
                self.player = None
                pause()
                break

    def inventory_text(self) -> str:
        if self.player is None or not self.player.inventory:
            return "empty"
        return ", ".join(item_name(item) for item in self.player.inventory)

    def show_info(self) -> None:
        clear()
        title("INFO", CYAN)
        msg("ADVENTURE is a CLI RPG.")
        msg(f"Explore {TOTAL_ROOMS} rooms and defeat the Crimson King.")
        msg(f"Mini bosses appear at rooms {MINI_BOSS_ROOMS[0]} and {MINI_BOSS_ROOMS[1]}.")
        msg("Merchant appears before the final stage.")
        msg(f"Final boss appears at room {FINAL_BOSS_ROOM}.")
        msg("Bosses become stronger when their HP drops below a threshold.")
        pause()

    def show_stats(self) -> None:
        if self.player is None:
            return
        clear()
        title("HERO STATS", CYAN)
        item_counts = {
            item_name(item): self.player.inventory.count(item)
            for item in set(self.player.inventory)
        }
        info_box(
            (
                f"Name: {self.player.name}",
                f"Room: {self.room_number} / {TOTAL_ROOMS}",
                f"HP: {self.player.hp} / {self.player.max_hp}",
                f"Armor: {self.player.armor}",
                f"Attack: {self.player.attack}",
                f"Temporary attack bonus: {self.player.attack_bonus}",
                f"Gold: {self.player.gold}",
                f"Inventory: {self.inventory_text()}",
                "Defeated enemies: "
                + (
                    ", ".join(self.player.defeated_enemies)
                    if self.player.defeated_enemies
                    else "none"
                ),
                f"Item counts: {item_counts if item_counts else 'empty'}",
            )
        )
        pause()

    def open_inventory(self) -> None:
        if self.player is None:
            return
        while True:
            selected_item = choose_inventory_item(self.player)
            if selected_item is None:
                return
            say(self.player.use_item(selected_item), code=GREEN)
            if not self.player.is_alive():
                raise GameOverError("The potion was your last mistake.")
            pause()

    def explore(self) -> None:
        if self.player is None:
            return

        self.room_number += 1
        clear()
        title("EXPLORATION", CYAN)
        self.player.visited_rooms.add(self.room_number)
        say(f"You open door #{self.room_number}.", code=CYAN)
        for text in random_exploration_lines():
            say(text)
        event = stage_event(self.room_number)
        pause()

        match event:
            case "enemy":
                start_fight(self.player, create_enemy())
            case "mini_boss":
                stage_number = 1 if self.room_number == MINI_BOSS_ROOMS[0] else 2
                start_fight(self.player, create_mini_boss(stage_number))
            case "final_boss":
                start_fight(self.player, create_final_boss())
                self.show_ending()
            case "treasure":
                self.find_treasure()
            case "trap":
                self.trigger_trap()
            case "potion":
                self.find_potion()
            case "empty":
                self.empty_room()
            case "merchant":
                self.meet_merchant()

    def empty_room(self) -> None:
        if self.player is None:
            return
        title("EMPTY ROOM")
        say(empty_room_text())
        if random.randint(1, 100) <= 25:
            gold = random.randint(3, 8)
            self.player.gold += gold
            msg(f"You found {gold} gold in the dust.", YELLOW)
        pause()

    def find_treasure(self) -> None:
        if self.player is None:
            return
        clear()
        title("TREASURE", YELLOW)
        gold = random.randint(10, 30)
        self.player.gold += gold
        say("You found an old chest.", code=YELLOW)
        msg(f"+{gold} gold", YELLOW)
        if random.randint(1, 2) == 1:
            potion = random_potion()
            self.player.add_item(potion)
            msg(f"+1 {item_name(potion)}", GREEN)
        pause()

    def find_potion(self) -> None:
        if self.player is None:
            return
        clear()
        title("ITEM", BLUE)
        potion = random_potion()
        self.player.add_item(potion)
        say("You found a forgotten bottle.", code=GREEN)
        msg(f"{item_name(potion)} added to inventory.", GREEN)
        pause()

    def trigger_trap(self) -> None:
        if self.player is None:
            return
        title("TRAP", RED)
        damage = random.randint(4, 10)
        real_damage = self.player.receive_hit(damage)
        say("You hear a sudden click.", code=RED)
        say("Spikes burst from the floor.", code=RED)
        if real_damage == 0:
            msg("Your armor blocked the trap.", BLUE)
        else:
            msg(f"You lost {real_damage} HP.", RED)
        if not self.player.is_alive():
            raise GameOverError("You died in a trap. Game over.")
        pause()

    def meet_merchant(self) -> None:
        if self.player is None:
            return
        while True:
            clear()
            title("WANDERING MERCHANT", YELLOW)
            msg("A tired merchant sits near a broken wall.", MUTED)
            msg(f"Your gold: {self.player.gold}", YELLOW)
            shop_options = [
                f"[{index}] {item_name(item)} - {item_price(item)} gold"
                for index, item in enumerate(SHOP_ITEMS, start=1)
            ]
            shop_options.append(f"[{len(SHOP_ITEMS) + 1}] Leave")
            choices(shop_options)
            choice = input("\nChoose option: ")

            if not choice.isdigit():
                msg("Wrong option.", RED)
                pause()
                continue
            number = int(choice)
            if number == len(SHOP_ITEMS) + 1:
                return
            if 1 <= number <= len(SHOP_ITEMS):
                self.buy_item(SHOP_ITEMS[number - 1])
                continue
            msg("Wrong option.", RED)
            pause()

    def buy_item(self, item_code: ItemCode) -> bool:
        if self.player is None:
            return False
        price = item_price(item_code)
        if self.player.gold < price:
            msg("You do not have enough gold.", RED)
            pause()
            return False
        self.player.gold -= price
        self.player.add_item(item_code)
        msg(f"Bought {item_name(item_code)}.", GREEN)
        pause()
        return True

    def show_ending(self) -> None:
        clear()
        title("THE END", GREEN)
        say("The Crimson King falls to the ground.", code=GREEN)
        say("The castle becomes silent.", code=GREEN)
        say("Your family is finally avenged.", code=GREEN)
        print(color("\n# You finished the adventure.", GREEN))
        self.finished = True
        pause()

    def save(self) -> None:
        if self.player is None:
            return
        clear()
        title("SAVE GAME", CYAN)
        try:
            save_game(GameState(self.player, self.room_number, self.finished))
            msg("Game saved successfully.", GREEN)
        except SaveFileError as error:
            msg(f"Error: {error}", RED)
        pause()

    def load(self) -> None:
        clear()
        title("LOAD GAME", CYAN)
        try:
            state = load_game()
            self.player = state.player
            self.room_number = state.room_number
            self.finished = state.finished
            msg(f"Welcome back, {self.player.name}.", GREEN)
        except SaveFileError as error:
            msg(f"Error: {error}", RED)
            self.player = None
        pause()
