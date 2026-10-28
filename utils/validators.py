"""Input validation helpers."""

import re

from utils.exceptions import InvalidHeroNameError

HERO_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,15}$")


def validate_hero_name(name: str) -> str:
    if HERO_NAME_PATTERN.fullmatch(name) is None:
        raise InvalidHeroNameError(
            "Name must be 3-15 characters and contain only letters, digits or underscore."
        )
    return name
