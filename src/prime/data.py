"""Откуда берём данные.

Сейчас — из снимка, в итоговом проекте — из учебной базы. Где лежит снимок,
решают настройки: функции получают папку параметром.
"""

import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def load_payments(data_dir: Path) -> pd.DataFrame:
    table = pd.read_csv(data_dir / "payments.csv", parse_dates=["paid_at"])
    log.info("Платежей прочитано: %d", len(table))
    return table


def load_subscriptions(data_dir: Path) -> pd.DataFrame:
    table = pd.read_csv(data_dir / "subscriptions.csv", parse_dates=["started_at", "ended_at"])
    log.info("Подписок прочитано: %d", len(table))
    return table
