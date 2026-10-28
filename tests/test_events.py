import core.events as events
from models.boss import Boss


def test_stage_events_have_fixed_milestones(monkeypatch):
    monkeypatch.setattr(events, "normal_event", lambda: "empty")
    assert events.stage_event(4) == "mini_boss"
    assert events.stage_event(8) == "mini_boss"
    assert events.stage_event(11) == "merchant"
    assert events.stage_event(13) == "final_boss"
    assert events.stage_event(3) == "empty"


def test_final_boss_has_enrage_mechanic():
    boss = events.create_final_boss()
    assert isinstance(boss, Boss)
    boss.take_damage(35)
    assert boss.enraged
    assert boss.get_total_attack() == 15
