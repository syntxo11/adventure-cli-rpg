"""Reusable terminal inventory selection."""

from __future__ import annotations

from models.item import ItemCode, item_name
from models.player import Player
from utils.ui import BLUE, RED, clear, msg, pause, title


def choose_inventory_item(player: Player) -> ItemCode | None:
    """Ask the player for an inventory item and return its code."""
    while True:
        clear()
        title("INVENTORY", BLUE)

        if not player.inventory:
            msg("Inventory is empty.")
            input("\nPress Enter to leave inventory...")
            return None

        for index, item in enumerate(player.inventory, start=1):
            print(f"[{index}] {item_name(item)}")

        choice = input("\nChoose item or press Enter to leave inventory: ")
        if choice == "":
            return None
        if not choice.isdigit():
            msg("Wrong option.", RED)
            pause()
            continue

        number = int(choice)
        if 1 <= number <= len(player.inventory):
            return player.inventory[number - 1]

        msg("Wrong option.", RED)
        pause()
