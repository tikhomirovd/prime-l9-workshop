"""Настройки: всё, что отличается от машины к машине, — в .env, а не в коде.

В коде остаются только значения по умолчанию. Пароли и токены в коде
не появляются вовсе: код уходит в git, а .env — нет.
"""

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    log_file: Path
    out_dir: Path
    state_file: Path
    replay_start: date
    # repr=False: токен не печатается, даже если напечатать настройки целиком
    telegram_token: str = field(repr=False)


def load_settings() -> Settings:
    load_dotenv(ROOT / ".env")
    return Settings(
        # ROOT / "data" — относительный путь от корня проекта; абсолютный путь в .env его заменит
        data_dir=ROOT / os.getenv("PRIME_DATA_DIR", "data"),
        log_file=ROOT / "logs" / "prime.log",
        out_dir=ROOT / "out",
        state_file=ROOT / "state" / "replay.json",
        replay_start=date.fromisoformat(os.getenv("PRIME_REPLAY_START", "2026-08-20")),
        telegram_token=os.getenv("TELEGRAM_TOKEN", ""),
    )
