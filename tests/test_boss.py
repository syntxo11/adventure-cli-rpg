from models.boss import Boss


def make_boss() -> Boss:
    return Boss(
        "Test Boss",
        max_hp=40,
        attack=8,
        gold_reward=10,
        dialogues=("Fight me",),
        enrage_threshold=0.5,
        enrage_bonus=3,
    )


def test_boss_starts_in_normal_phase():
    boss = make_boss()
    assert boss.phase_name == "NORMAL"
    assert boss.get_total_attack() == 8


def test_boss_enrages_below_threshold():
    boss = make_boss()
    boss.take_damage(20)
    assert boss.enraged
    assert boss.phase_name == "ENRAGED"
    assert boss.get_total_attack() == 11
