import pytest
from conftest import load

solve = load(5).sprint_calendar


def test_start_on_weekend():
    """Перевірка старту у вихідний день (субота): спринт має початися з найближчого робочого дня (понеділок)."""
    res = solve("2026-11-07", 5, 1, [])
    assert res["sprints"][0]["start"] == "2026-11-09"
    assert res["sprints"][0]["end"] == "2026-11-13"
    assert res["calendar_days"] == 5


def test_holiday_on_weekend_ignored():
    """Свято, що припадає на вихідний день, не повинно подовжувати або зсувати робочі дні спринту."""
    # 2026-11-14 — субота
    res = solve("2026-11-09", 5, 1, ["2026-11-14"])
    assert res["sprints"][0]["start"] == "2026-11-09"
    assert res["sprints"][0]["end"] == "2026-11-13"
    assert res["calendar_days"] == 5


def test_invalid_date_format():
    """Граничний випадок валідації: некоректний формат дати або неіснуючий календарний день."""
    with pytest.raises(ValueError, match="Недопустима дата: 2026-02-30"):
        solve("2026-02-30", 10, 2, [])

    with pytest.raises(ValueError, match="Недопустима дата: 2026-1-1"):
        solve("2026-1-1", 10, 2, [])


def test_invalid_days_and_count():
    """Граничний випадок валідації: не додатні цілі або boolean параметри."""
    with pytest.raises(ValueError, match="Тривалість спринту має бути додатною"):
        solve("2026-12-14", 0, 2, [])

    with pytest.raises(ValueError, match="Тривалість спринту має бути додатною"):
        solve("2026-12-14", True, 2, [])

    with pytest.raises(ValueError, match="Кількість спринтів має бути додатною"):
        solve("2026-12-14", 10, -1, [])