"""Откуда берём данные.

Сейчас — из снимка, в итоговом проекте — из учебной базы. Где лежит снимок,
решают настройки: функции получают папку параметром.
"""

from pathlib import Path

import pandas as pd


def load_payments(data_dir: Path) -> pd.DataFrame:
    return pd.read_csv(data_dir / "payments.csv", parse_dates=["paid_at"])


def load_subscriptions(data_dir: Path) -> pd.DataFrame:
    return pd.read_csv(data_dir / "subscriptions.csv", parse_dates=["started_at", "ended_at"])
