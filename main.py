"""ADVENTURE application entry point."""

from core.game import Game


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
