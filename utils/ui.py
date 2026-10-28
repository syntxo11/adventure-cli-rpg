# utils/ui.py
# Console UI: titles, colors, slow dialogue.

import os
import time

WIDTH = 60

RESET = "\033[0m"

# Soft, readable colors. Not neon.
TEXT = "\033[38;5;250m"
MUTED = "\033[38;5;245m"
RED = "\033[38;5;167m"
GREEN = "\033[38;5;108m"
YELLOW = "\033[38;5;179m"
BLUE = "\033[38;5;110m"
PURPLE = "\033[38;5;139m"
CYAN = "\033[38;5;116m"

ADVENTURE_LOGO = r"""
█████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗
██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝
██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗
╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝                                                                                                                                                                                                         
 
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def color(text, code):
    return f"{code}{text}{RESET}"


def msg(text="", code=None):
    """Print normal message with # prefix."""
    if code is None:
        print(f"# {text}")
    else:
        print(color(f"# {text}", code))


def pause():
    input("\n# Press Enter to continue...")


def say(text, delay=0.025, prefix="# ", code=None):
    """Print slow text for story/dialogue."""
    if code is not None:
        print(code, end="", flush=True)

    print(prefix, end="", flush=True)

    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)

    if code is not None:
        print(RESET, end="")

    print()


def title(text, code=None):
    if code is not None:
        print(code, end="")

    print()
    print("┌" + "─" * WIDTH + "┐")
    print("│" + text.center(WIDTH) + "│")
    print("└" + "─" * WIDTH + "┘")

    if code is not None:
        print(RESET, end="")


def victory_title():
    print(GREEN, end="")
    print()
    print("+" + "─" * WIDTH + "+")
    print("│" + "VICTORY".center(WIDTH) + "│")
    print("+" + "─" * WIDTH + "+")
    print(RESET, end="")


def info_box(lines):
    print("┌" + "─" * WIDTH + "┐")
    for text in lines:
        print("│ " + text[:WIDTH - 2].ljust(WIDTH - 2) + " │")
    print("└" + "─" * WIDTH + "┘")


def choices(options):
    print()
    padding = 22
    for option in options:
        print(" " * padding + option)
