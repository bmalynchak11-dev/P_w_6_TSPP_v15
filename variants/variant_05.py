"""
Задача 5. Календар спринтів і дата релізу.
"""

from datetime import date, timedelta


def _validate_iso_date(d_str: str) -> date:
    """Перевіряє, чи є рядок коректною датою у форматі YYYY-MM-DD з 10 символів."""
    if not isinstance(d_str, str) or len(d_str) != 10:
        raise ValueError(f"Недопустима дата: {d_str}")
    try:
        parts = d_str.split("-")
        if len(parts) != 3 or len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
            raise ValueError(f"Недопустима дата: {d_str}")
        return date.fromisoformat(d_str)
    except Exception:
        raise ValueError(f"Недопустима дата: {d_str}")


def _is_working_day(d: date, holidays_set: set[date]) -> bool:
    """Робочий день — це понеділок–п'ятниця (weekday < 5), що не є у списку свят."""
    return d.weekday() < 5 and d not in holidays_set


def _next_working_day(d: date, holidays_set: set[date]) -> date:
    """Повертає найближчий робочий день, починаючи з дати d включно."""
    curr = d
    while not _is_working_day(curr, holidays_set):
        curr += timedelta(days=1)
    return curr


def sprint_calendar(start: str, days: int, count: int, holidays: list) -> dict:
    """
    Перетворює спринти на календарну дату релізу з урахуванням вихідних і свят.
    """
    # 1. Перевірка start
    start_date = _validate_iso_date(start)

    # 2. Перевірка дат у holidays
    holiday_dates = set()
    for h in holidays:
        h_date = _validate_iso_date(h)
        holiday_dates.add(h_date)

    # 3. Перевірка days (строго ціле число, bool відхиляється)
    if isinstance(days, bool) or not isinstance(days, int) or days < 1:
        raise ValueError("Тривалість спринту має бути додатною")

    # 4. Перевірка count (строго ціле число, bool відхиляється)
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError("Кількість спринтів має бути додатною")

    sprints = []
    current_search_date = start_date

    for i in range(1, count + 1):
        # Початок спринту — перший робочий день, не раніше current_search_date
        sprint_start = _next_working_day(current_search_date, holiday_dates)

        # Відлічуємо days робочих днів
        curr = sprint_start
        working_days_counted = 1

        while working_days_counted < days:
            curr += timedelta(days=1)
            if _is_working_day(curr, holiday_dates):
                working_days_counted += 1

        sprint_end = curr
        sprints.append({
            "n": i,
            "start": sprint_start.isoformat(),
            "end": sprint_end.isoformat(),
        })

        # Наступний спринт починається після кінця попереднього
        current_search_date = sprint_end + timedelta(days=1)

    release_date = sprints[-1]["end"]
    first_sprint_start = date.fromisoformat(sprints[0]["start"])
    last_sprint_end = date.fromisoformat(release_date)

    # Календарні дні від початку 1-го спринту до дати релізу включно
    calendar_days = (last_sprint_end - first_sprint_start).days + 1

    return {
        "sprints": sprints,
        "release": release_date,
        "calendar_days": calendar_days,
    }


if __name__ == "__main__":
    res = sprint_calendar(
        start="2026-12-14",
        days=10,
        count=2,
        holidays=["2026-12-25", "2027-01-01", "2027-01-07"],
    )
    print(res)