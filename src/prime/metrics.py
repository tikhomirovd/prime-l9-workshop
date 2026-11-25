"""Что считаем: показатели за день и за период.

Функции получают таблицу и даты и возвращают число. Откуда пришли данные
и куда уйдёт результат, они не знают, поэтому их легко проверить
на игрушечной таблице и вызвать из отчёта, из повторного прогона и из бота.
Дни считаются по UTC: в этом поясе время хранится в базе ПРАЙМ.
"""

from datetime import date

import pandas as pd


def revenue(payments: pd.DataFrame, start: date, end: date) -> float:
    """Выручка по успешным платежам с start по end включительно."""
    paid = payments[payments["status"] == "success"]
    day = paid["paid_at"].dt.date
    in_period = (day >= start) & (day <= end)
    return float(paid.loc[in_period, "amount"].sum())


def new_subscriptions(subscriptions: pd.DataFrame, day: date) -> int:
    """Сколько подписок оформлено в этот день."""
    return int((subscriptions["started_at"].dt.date == day).sum())


def daily_ticket(payments: pd.DataFrame, day: date) -> tuple[int, float | None]:
    """Количество успешных платежей и их средняя сумма за день UTC."""
    today = payments.loc[payments["paid_at"].dt.date == day]
    successful = today.loc[today["status"] == "success", "amount"]
    count = len(today)
    return count, float(successful.sum()) / count if count else None
