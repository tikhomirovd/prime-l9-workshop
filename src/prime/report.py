"""Отчёт за дату: собрать показатели и превратить их в текст.

Дата отчёта — это день, когда отчёт читают. Описывает он вчерашний день
и неделю, которая вчера закончилась: за сегодня данных ещё нет.
"""

from datetime import date, timedelta

from prime import data, metrics


def build_day(report_date: date) -> dict:
    """Показатели для отчёта: вчерашний день и неделя до него."""
    day = report_date - timedelta(days=1)
    payments = data.load_payments()
    subscriptions = data.load_subscriptions()
    print(f"Загружено: {len(payments)} платежей, {len(subscriptions)} подписок")
    return {
        "report_date": report_date.isoformat(),
        "day": day.isoformat(),
        "revenue_day": metrics.revenue(payments, day, day),
        "revenue_7d": metrics.revenue(payments, day - timedelta(days=6), day),
        "new_subscriptions": metrics.new_subscriptions(subscriptions, day),
    }


def rub(amount: float) -> str:
    """12345.6 -> '12 345,60 ₽'"""
    return f"{amount:,.2f} ₽".replace(",", " ").replace(".", ",")


def format_report(row: dict) -> str:
    report_date = date.fromisoformat(row["report_date"])
    day = date.fromisoformat(row["day"])
    return "\n".join([
        f"ПРАЙМ, отчёт на {report_date:%d.%m.%Y} — данные за {day:%d.%m.%Y}, UTC",
        f"  выручка за день     {rub(row['revenue_day']):>14}",
        f"  выручка за 7 дней   {rub(row['revenue_7d']):>14}",
        f"  новых подписок      {row['new_subscriptions']:>12}",
    ])
