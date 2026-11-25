"""Контрольные примеры С9. Запуск: python -m unittest discover -s tests -v."""

import unittest
from datetime import date

import pandas as pd

from prime.metrics import daily_ticket


class DailyTicketTest(unittest.TestCase):
    """Что обещает строка «средний успешный платёж за день UTC»."""

    def setUp(self) -> None:
        """Два успешных платежа, отказ и платёж уже следующего дня."""
        self.day = date(2026, 8, 23)
        self.payments = pd.DataFrame({
            "paid_at": pd.to_datetime([
                "2026-08-23 00:00:00", "2026-08-23 12:00:00",
                "2026-08-23 23:59:59", "2026-08-24 00:00:00",
            ], utc=True),
            "amount": [100, 300, 900, 700],
            "status": ["success", "success", "failed", "success"],
        })

    def test_average_for_day(self) -> None:
        """Среднее за 23 августа считается по двум успешным платежам."""
        self.assertEqual(daily_ticket(self.payments, self.day), (2, 200.0))

    def test_only_failures(self) -> None:
        """При одних отказах число успехов равно нулю, среднего нет."""
        failures = self.payments.assign(status="failed")
        self.assertEqual(daily_ticket(failures, self.day), (0, None))

    def test_midnight(self) -> None:
        """Платёж в полночь UTC входит в следующий день."""
        self.assertEqual(daily_ticket(self.payments, date(2026, 8, 24)), (1, 700.0))
