"""Откуда берём данные.

Сейчас — из снимка в папке data/, в итоговом проекте — из учебной базы.
Когда источник поменяется, править придётся только этот файл: остальной код
получает готовые таблицы и не знает, где они лежали.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_payments(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_csv(data_dir / "payments.csv", parse_dates=["paid_at"])


def load_subscriptions(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_csv(data_dir / "subscriptions.csv", parse_dates=["started_at", "ended_at"])
