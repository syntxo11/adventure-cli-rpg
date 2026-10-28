import pytest

from utils.exceptions import InvalidHeroNameError
from utils.validators import validate_hero_name


@pytest.mark.parametrize("name", ["Hero", "player_1", "ABC123", "abc"])
def test_valid_hero_names(name):
    assert validate_hero_name(name) == name


@pytest.mark.parametrize("name", ["ab", "name!", "with space", "abcdefghijklmnop"])
def test_invalid_hero_names(name):
    with pytest.raises(InvalidHeroNameError):
        validate_hero_name(name)
